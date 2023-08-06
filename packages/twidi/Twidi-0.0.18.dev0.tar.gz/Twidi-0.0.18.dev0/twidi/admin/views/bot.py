import json
import threading
from threading import Thread
from time import sleep

import requests
from flask import Response, redirect
from flask_admin import expose, BaseView

from twidi.admin import app
from twidi.admin.data import load_redemptions_from_json
from twidi.admin.models import Configuration, Command, Cog

# Flask and Flask-SQLAlchemy initialization here
from twidi.twitch.midi_bot import MidiCommand


class BotView(BaseView):
    bot_thread = None

    @expose("/")
    def index(self):
        import twidi.admin.bot
        bot = twidi.admin.bot.bot
        loaded_commands = bot.get_loaded_command_help()
        loaded_redemptions = bot.get_loaded_redemption_help()
        bot_running = bot.loop.is_running()
        loaded_cogs = []
        unloaded_cogs = []
        bot_loaded_cogs = bot.twidi_cogs
        all_cogs = self.session.query(Cog).all()
        for cog in all_cogs:
            if cog.label in bot_loaded_cogs:
                loaded_cogs.append(cog)
            else:
                unloaded_cogs.append(cog)

        return self.render(
            "bot.html", data={'app': app, 'status': bot_running, 'loaded_commands': loaded_commands,
                              'loaded_redemptions': loaded_redemptions, 'loaded_cogs': loaded_cogs,
                              'unloaded_cogs': unloaded_cogs}
        )

    def __init__(self, session, **kwargs):
        super().__init__(**kwargs)
        self.session = session

    @expose('/load_cog/<cog_id>', methods=['GET', 'POST'])
    def load_cog(self, cog_id=None):
        import twidi.admin.bot
        bot = twidi.admin.bot.bot
        cog = self.session.query(Cog).filter(Cog.id == int(cog_id)).first()
        bot.load_cog(cog=cog, reload=True)
        for command in cog.commands:
            bot.load_twidi_command(command=MidiCommand(command=command))
        # Quick hack to give the bot time to load
        sleep(1)
        return Response(status=200)

    @expose("/unload_cog/<cog_id>", methods=['POST'])
    def unload_cog(self, cog_id):
        import twidi.admin.bot
        bot = twidi.admin.bot.bot
        cog = self.session.query(Cog).filter(Cog.id == int(cog_id)).first()
        bot.unload_cog(cog=cog)
        # Quick hack to give the bot time to load
        sleep(1)
        return Response(status=200)

    @expose('/start_bot', methods=['POST'])
    def start_bot(self):
        import twidi.admin.bot
        bot = twidi.admin.bot.bot
        if not self.bot_thread:
            self.bot_thread = threading.Thread(target=bot.run, daemon=True)
        self.bot_thread.start()
        # Quick hack to give the bot time to start
        sleep(1)
        return Response(status=200)

    @expose(url='/redemptions', methods=['POST'])
    def redemptions(self):
        config: Configuration = self.session.query(Configuration).first()
        url = 'https://api.twitch.tv/helix/channel_points/custom_rewards'
        client_id_header = {'Client-Id': config.broadcaster_client_token}
        client_auth_header = dict({'Authorization': 'Bearer {}'.format(config.broadcaster_access_token)})
        headers = dict()
        headers.update(client_id_header)
        headers.update(client_auth_header)
        response = requests.get(url=url, params={'broadcaster_id': str(config.broadcaster_id)}, headers=headers)
        load_redemptions_from_json(json.loads(response.content))
        return Response(status=200, content_type='application/json', response=response.text)

    @expose(url='/load_commands', methods=('GET',))
    def refresh_redemption_list(self):
        return

    @expose(url='/restart_bot', methods=('GET',))
    def refresh_redemption_list(self):
        return
