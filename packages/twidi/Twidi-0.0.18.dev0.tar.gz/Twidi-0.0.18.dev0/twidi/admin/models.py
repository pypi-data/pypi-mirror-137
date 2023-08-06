from __future__ import annotations

import mido
from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship

from twidi.admin import db
from twidi.device.devices import MidiMessageType

"""
===========  ======================  ================
Name         Valid Range             Default Value
===========  ======================  ================
channel      0..15                   0
frame_type   0..7                    0
frame_value  0..15                   0
control      0..127                  0
note         0..127                  0
program      0..127                  0
song         0..127                  0
value        0..127                  0
velocity     0..127                  64
data         (0..127, 0..127, ...)   () (empty tuple)
pitch        -8192..8191             0
pos          0..16383                0
time         any integer or float    0
===========  ======================  ================
"""

# from twidi.admin.base import Base
cog_command_association = Table(
    "cog_command",
    db.metadata,
    Column("cog_id", Integer, ForeignKey("cog.id")),
    Column("command_id", Integer, ForeignKey("command.id")),
)

"""
device_message_association = Table(
    "device_command",
    db.metadata,
    Column("device_id", Integer, ForeignKey("device.id")),
    Column("command_id", Integer, ForeignKey("command.id")),
)
"""


class Device(db.Model):
    __tablename__ = "device"

    id = db.Column(Integer, primary_key=True)
    label = db.Column(String)
    device_id = db.Column(String, unique=True)
    midi_message = db.relationship("MidiMessage", back_populates="device")

    def __repr__(self):
        return "<Device(device_id='%s', label='%s')>" % (self.device_id, self.label)


# Aggregates commands into a collection for loading
class Cog(db.Model):
    __tablename__ = "cog"
    id = Column(Integer, primary_key=True)
    prefix = Column(String)
    label = Column(String)
    enabled = Column(Boolean)
    commands = relationship("Command", secondary=cog_command_association)


# Represents text triggers for commands
class CommandTrigger(db.Model):
    __tablename__ = "command_trigger"
    id = Column(Integer, primary_key=True, autoincrement=True)
    trigger_text = Column(String)
    command_id = Column(Integer, ForeignKey("command.id"))
    command = relationship("Command", back_populates="command_trigger")

    def __repr__(self):
        return "<Trigger(command='%s', trigger_text='%s')>" % (
            self.command,
            self.trigger_text,
        )


# Represents Twitch bot credentials, channel, etc
# TODO Salt/hash these values
class Configuration(db.Model):
    id = Column(Integer, primary_key=True)
    broadcaster_id = Column(Integer)
    # Twidi bot prefix
    bot_global_prefix = Column(String, default='twidi')

    # For grabbing channel redemptions/points/bits/sub info
    broadcaster_access_token = Column(String)
    broadcaster_client_token = Column(String)
    broadcaster_refresh_token = Column(String)
    # For interacting with chat / reading chat
    bot_access_token = Column(String)
    bot_refresh_token = Column(String)
    bot_client_token = Column(String)
    channel_id = Column(String)


# Represents the command that the Twitch bot will execute
class Command(db.Model):
    __tablename__ = "command"
    id = Column(Integer, primary_key=True)
    description = Column(String, default="")
    label = Column(String(50))
    success_message = Column(String, nullable=True)
    cooldown_message = Column(String, nullable=True)
    failure_message = Column(String, nullable=True)
    mod_only = Column(Boolean, default=False)
    cool_down_in_seconds = Column(Integer, default=0)
    message_id = Column(Integer, ForeignKey("midi_message.id"))
    midi_message = relationship("MidiMessage")
    command_trigger = db.relationship(
        "CommandTrigger", uselist=True, back_populates="command"
    )

    point_redemption = db.relationship("PointRedemption", back_populates="command", uselist=False)

    def __repr__(self):
        return "<Command(id='%s', label='%s, description='%s')>" % (self.id, self.label, self.description)


class PointRedemption(db.Model):
    __tablename__ = "point_redemption"
    id = Column(String, primary_key=True)
    command_id = Column(Integer, ForeignKey("command.id"))
    enabled = Column(Boolean)
    title = Column(String)
    prompt = Column(String)
    command = db.relationship("Command", back_populates="point_redemption")
    is_user_input_required = Column(Boolean)
    cooldown_in_seconds = Column(Integer)
    cost = Column(Integer)

    def __repr__(self):
        return "<Redemption(title='%s)>" % (self.title)


class MidiMessage(db.Model):
    __tablename__ = "midi_message"
    id = Column(Integer, primary_key=True)
    label = Column(String(50))
    channel = Column(Integer, default=0)
    type = Column(String(50))
    device_id = Column(Integer, ForeignKey("device.id"))
    device = relationship("Device", back_populates="midi_message")
    __mapper_args__ = {"polymorphic_identity": "midi_message", "polymorphic_on": type}


class ControlMessage(MidiMessage):
    __tablename__ = "control_message"
    control_id = Column(Integer, ForeignKey("midi_message.id"), primary_key=True)
    default_value = Column(Integer, default=0)
    curve_duration_in_seconds = Column(Integer, default=0)
    calibration_value = Column(Integer, default=0)
    min_value = Column(Integer, default=0)
    max_value = Column(Integer, default=127)
    value = Column(Integer, default=0)
    cc_number = Column(Integer, default=0)
    __mapper_args__ = {
        "polymorphic_identity": MidiMessageType.CONTROL_CHANGE.value,
    }

    def to_midi_message(self, **kwargs):
        """TODO Allow overwriting"""
        args = dict(kwargs)
        if 'value' in args.keys():
            args.update({'value': int(args.get('value'))})
            args.pop('value')

        message_data = {
            'value': self.value,
            'channel': self.channel,
            'type': MidiMessageType.CONTROL_CHANGE.value,
            'control': self.cc_number,
        }

        if 'channel' in args.keys():
            args['channel'] = int(args['channel'])
        if 'value' in args.keys():
            args['value'] = int(args['value'])
        if 'cc_number' in args.keys():
            args['cc_number'] = int(args['cc_number'])

        message_data.update(args)
        return mido.Message(**message_data)

    def __repr__(self):
        return "<ControlMessage(id='%s', label='%s', cc_number='%s', channel='%s')>" % (
            self.id,
            self.label,
            self.cc_number,
            self.channel,

        )


class NoteMessage(MidiMessage):
    __tablename__ = "note_message"
    note_message_id = Column(Integer, ForeignKey("midi_message.id"), primary_key=True)
    default_value = Column(Integer, default=0)
    min_value = Column(Integer, default=0)
    max_value = Column(Integer, default=127)
    value = Column(Integer, default=0)
    velocity = Column(Integer, default=127)
    pitch = Column(Integer, default=100)
    duration = Column(Integer, default=0)
    __mapper_args__ = {
        "polymorphic_identity": MidiMessageType.NOTE_ON.value,
    }

    def to_midi_message(self, **kwargs):
        """TODO Allow overwriting"""
        args = dict(kwargs)
        if 'value' in args.keys():
            args.update({'note': args.get('value')})
            args.pop('value')

        message_data = {
            'note': self.value,
            'velocity': self.velocity,
            'channel': self.channel,
            'type': MidiMessageType.NOTE_ON.value,
        }
        message_data.update(args)
        return mido.Message(**message_data)

    def __repr__(self):
        return "<NoteMessage(id='%s', label='%s', value='%s', channel='%s')>" % (
            self.id,
            self.label,
            self.value,
            self.channel,
        )


class ProgramMessage(MidiMessage):
    __tablename__ = "program_message"
    program_message_id = Column(Integer, ForeignKey("midi_message.id"), primary_key=True)
    default_value = Column(Integer, default=0)
    value = Column(Integer, default=0, comment='Represents the program value')
    __mapper_args__ = {
        "polymorphic_identity": MidiMessageType.PROGRAM_CHANGE.value,
    }

    def to_midi_message(self, **kwargs):
        """TODO Allow overwriting"""
        args = dict(kwargs)
        if 'value' in args.keys():
            args.update({'program': args.get('value')})
            args.pop('value')

        message_data = {
            'program': self.value,
            'channel': self.channel,
            'type': MidiMessageType.PROGRAM_CHANGE.value,
        }
        message_data.update(args)
        return mido.Message(**message_data)

    def __repr__(self):
        return "<ProgramMessage(id='%s', label='%s', program='%s', channel='%s')>" % (
            self.id,
            self.label,
            self.program,
            self.channel,
        )


class BpmMessage(MidiMessage):
    __tablename__ = "bpm_message"
    bpm_message_id = Column(Integer, ForeignKey("midi_message.id"), primary_key=True)
    default_value = Column(Integer, default=0)
    value = Column(Integer, default=0)
    __mapper_args__ = {
        "polymorphic_identity": MidiMessageType.BPM.value,
    }

    def to_midi_message(self, **kwargs):
        """TODO Check BPM SPEC
        args = dict(kwargs)
        if 'value' in args.keys():
            args.update({'program': args.get('value')})
            args.pop('value')

        message_data = {
            'program': self.value,
            'channel': self.channel,
            'type': MidiMessageType.NOTE_ON.value,
        }
        message_data.update(args)
        return mido.Message(**message_data)
        """
        return None

    def __repr__(self):
        return "<BpmMessage(id='%s', label='%s', value='%s', channel='%s')>" % (
            self.id,
            self.label,
            self.value,
            self.channel,
        )
# """
# session = Session()
# session.close()
# """
