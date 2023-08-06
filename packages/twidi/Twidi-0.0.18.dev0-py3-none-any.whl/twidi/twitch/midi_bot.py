import datetime
import logging
import sys
import threading

import mido
import twitchio.ext.commands
from twitchio.cooldowns import RateBucket
from twitchio.ext import commands
from twitchio.ext.commands import Cooldown, Context
from twitchio.ext.commands.cooldowns import Bucket as CooldownBucket

from twidi.admin import db
from twidi.admin.models import Command, NoteMessage, ControlMessage, MidiMessage, Configuration, Cog
from twidi.device.devices import DeviceManager, device_manager, MidiMessageType

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.INFO)

"""
Backlog
    A single command parsed from the database.
    The command will have access to the device it needs
    The command will handle triggers
    The command will handle cool-downs
    The command will handle permissions
"""


class MidiInterface:

    def test_midi_message(self, form, create_model, value=None):
        message = create_model(form)
        value_to_send = None
        device_id = None
        try:
            value_to_send = message.value
        except Exception:
            value_to_send = value
        try:
            device_id = message.device.device_id
        except Exception:
            device_id = None

        logger.info('Sending test message {} with value: {} to device: {} '.format(message, value, device_id))
        device_manager.send_midi_message(
            message=message.to_midi_message(value=value_to_send), device_id=device_id
        )

    def panic_device(self, device_id=None):
        device_manager.send_midi_message(device_id=device_id, message=mido.Message(type='reset'))

    def send_midi_message(self, message: MidiMessage, value=None, use_current=False, commit=True, **kwargs):
        if use_current:
            value_to_send = message.value
        else:
            value_to_send = value if value else message.default_value
        value_to_send = int(value_to_send)
        if message.type == MidiMessageType.NOTE_ON.value:
            self.send_note_message(message, value_to_send, **kwargs)
        if message.type == MidiMessageType.CONTROL_CHANGE.value:
            self.send_control_message(message, value_to_send, **kwargs)
            if commit:
                message.value = value_to_send
                db.session.commit()

    def send_control_message(self, message: ControlMessage, value=None, **kwargs):
        logger.info('Sending control message {} with value {}'.format(message, value))
        device_manager.send_midi_message(
            message=message.to_midi_message(value=value), device_id=message.device.device_id
        )

        ''' TODO Determine curve duration - needs to figure out the math 
        Check out the Java Library bees was talking about
        if message.curve_duration:
            diff = int(abs(message.value - value))
            if diff > 1:
                per_second_diff = message.curve_duration / diff * 1000

                device_manager.send_midi_message(message=m, device_id=message.device_id)
                t = threading.Timer(interval=1, send_message, args=[m])
                t.start()
        
        '''

    def send_note_message(self, message: NoteMessage, value=None, **kwargs):
        logger.info('Sending note message {} with value {}'.format(message, value))
        DeviceManager.send_midi_message(message=message.to_midi_message(value=value))
        duration = message.duration
        if duration is not None:
            m = message.to_midi_message(type="note_off", value=value)
            def send_message(m):
                device_manager.send_midi_message(message=m, device_id=message.device.device_id)

            t = threading.Timer(duration, send_message, args=[m])
            t.start()


class MidiCommand(twitchio.ext.commands.Command):
    error_message = "Sorry buddy, could not run {}!"
    success_message = "Successfully changed {}, dude."
    cool_down_message = "Dude...{} is on cooldown for another {} seconds."
    midi_handler = MidiInterface()
    _twitch_command = None
    last_called = None
    session = None

    def __init__(self, command: Command):
        session = db.session
        command = session.query(Command).filter(Command.id == command.id).first()
        triggers = command.command_trigger
        aliases = [t.trigger_text for t in triggers if t.trigger_text != command.label]
        self.command = command
        self.is_redemption = command.point_redemption
        super(MidiCommand, self).__init__(name=command.label, aliases=aliases, func=self.handle_command)

    def is_off_cooldown(self):
        if not self.last_called or not self.command.cooldown_in_seconds:
            return True
        time_since_call = datetime.datetime.now() - self.last_called
        return time_since_call.seconds > self.command.cooldown_in_seconds

    def set_from_db_command(self, command, is_redemption):
        self.last_called = None
        self.set_command(command)
        if not is_redemption:
            self.set_command(command)

    def set_command(self, command: Command):
        triggers = command.command_trigger
        c = twitchio.ext.commands.Command(
            name=command.label,
            func=self.handle_command,
            aliases=[t.trigger_text for t in triggers if t.trigger_text != command.label],
        )
        c._cooldowns.append(
            Cooldown(
                bucket=CooldownBucket.channel,
                per=command.cool_down_in_seconds,
                rate=RateBucket.HTTP,
            )
        )
        return c

    async def handle_command(self, ctx: Context, value=None):
        logger.info("Running Command: {}".format(self.command))
        is_redemption = self.command.point_redemption and self.command.point_redemption.enabled
        mod_only = self.command.mod_only

        # Check if command is mod only
        if not ctx.author.is_mod and mod_only:
            logger.info('Abandoning command {}. Mod only.'.format(self.command))

        # Check if it is a redemption
        if is_redemption:
            if not ctx.author.is_mod:
                await ctx.reply(
                    content='Only a mod can do that. Chill.'

                )

        # Check if it is off cooldown (or user is a mod)
        if not ctx.author.is_mod and not self.is_off_cooldown():
            time_since_call = datetime.datetime.now() - self.last_called
            await ctx.reply(
                content=str(
                    self.cool_down_message.format(
                        self._twitch_command.full_name,
                        str(self.command.cooldown_in_seconds - time_since_call.seconds),
                    )
                )
            )

        try:
            # TODO Handle more than value parameters
            # TODO Ask about different MIDI inputs
            self.command = db.session.query(Command).filter(Command.id == self.command.id).first()
            self.midi_handler.send_midi_message(self.command.midi_message, value=value)
            self.last_called = datetime.datetime.now()
            await ctx.reply(self.success_message.format(self.command.label))

        except Exception as e:
            return await ctx.reply(self.error_message.format(e))


class TwidiBot(commands.Bot):
    """
    Bot for interacting with Eyesy
    """

    twidi_commands = dict()
    twidi_cogs = dict()

    def __init__(
            self,
            config: Configuration,
            **kwargs,
    ):
        token = config.bot_access_token
        self.prefix = '!twidi'
        initial_channel = config.channel_id
        super().__init__(
            token=token, prefix=self.prefix, **kwargs, initial_channels=['grogoyle']
        )

    def unload_cog(self, cog: Cog):
        if cog.label in self.twidi_cogs.keys():
            for command in cog.commands:
                if command.label in self.commands.keys():
                    self.remove_command(command.label)
            self.twidi_cogs.pop(cog.label)

    def load_cog(self, cog: Cog, reload):
        for command in cog.commands:
            self.load_twidi_command(command=MidiCommand(command), reload=reload)
        self.twidi_cogs.update({cog.label: cog})

    async def handle_commands(self, message):
        if 'about' in message.content:
            about_info = '''
            Twidi - A Twidi-to-Midi interface. Currently in beta. Project updates can be found at: https://twitter.com/Twidi02341695   
            '''
            context = await self.get_context(message=message, cls=None)
            await context.reply(about_info)
        if 'help' in message.content:
            context = await self.get_context(message=message, cls=None)
            help_lines = self.get_loaded_command_help()
            await context.reply(''.join(help_lines))

        print('Loaded commands {}'.format(self.commands.keys()))
        print('Recieved Message: {}'.format(message.content))
        context = await self.get_context(message)
        await self.invoke(context)

    def load_twidi_command(self, command: MidiCommand, reload=True):
        if reload:
            if command.name in self.commands.keys():
                self.commands.pop(command.name)
        self.add_command(command=command)

    def get_loaded_redemption_help(self):
        return self.get_loaded_command_help(redemptions=True)

    def get_loaded_command_help(self, redemptions=False):
        help_lines = []
        for name, command in self.commands.items():
            if not redemptions and command.command.point_redemption:
                continue
            if redemptions and not command.command.point_redemption:
                continue
            c: MidiCommand = command

            aliases = c.aliases
            description = c.command.description
            help_line = ' MrDestructoid {}'.format(description)
            if not aliases:
                aliases = [name]
            help_line += ' copyThis Triggers [{}] --'.format('!twidi '.join(aliases))
            help_lines.append(help_line)
        return help_lines

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
