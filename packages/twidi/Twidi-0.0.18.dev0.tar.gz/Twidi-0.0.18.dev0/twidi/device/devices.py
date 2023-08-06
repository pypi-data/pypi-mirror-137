import dataclasses
from enum import Enum

import mido
from mido import Backend

'''
Message Types
=============

Supported Messages
------------------

==============  ==============================
Name            Keyword Arguments / Attributes
==============  ==============================
note_off        channel note velocity
note_on         channel note velocity
polytouch       channel note value
control_change  channel control value
program_change  channel program
aftertouch      channel value
pitchwheel      channel pitch
sysex           data
quarter_frame   frame_type frame_value
songpos         pos
song_select     song
tune_request
clock
start
continue
stop
active_sensing
reset
==============  ==============================

``quarter_frame`` is used for SMPTE time codes. See:
http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/MTC.htm


Parameter Types
---------------

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

.. note::

    Mido numbers channels 0 to 15 instead of 1 to 16. This makes them
    easier to work with in Python but you may want to add and subtract
    1 when communicating with the user.

``velocity`` is how fast the note was struck or released. It defaults
to 64 so that if you don't set it, you will still get a reasonable
value. (64 is the recommended default for devices that don't support
it attack or release velocity.)

The ``time`` is used in MIDI files as delta time.

The ``data`` parameter accepts any iterable that generates numbers in
0..127. This includes::

    mido.Message('sysex', data=[1, 2, 3])
    mido.Message('sysex', data=range(10))
    mido.Message('sysex', data=(i for i in range(10) if i % 2 == 0))

For details about the binary encoding of a MIDI message, see:

http://www.midi.org/techspecs/midimessages.php
'''


class MidiMessageType(Enum):
    """
    The available MIDI message types
    """

    NO_TYPE = "undefined"
    PITCH_WHEEL = "pitchwheel"
    NOTE_ON = "note_on"
    NOTE_OFF = "note_off"
    CONTROL_CHANGE = "control_change"
    POLY_TOUCH = "polytouch"
    AFTER_TOUCH = "aftertouch"
    PROGRAM_CHANGE = "program_change"
    CLOCK = "clock"
    START = "start"
    RESET = "reset"
    STOP = "stop"
    CONTINUE = "continue"
    BPM = 'bpm'


@dataclasses.dataclass
class MessageData():
    message_type: str
    value: any
    channel: int = 0
    velocity: int = 127
    pitch: int = 0


class DeviceManager:
    __instance = None
    _device_out_ports = dict()

    @staticmethod
    def getInstance(backend: str = None, load=True):
        """Static access method."""
        if not DeviceManager.__instance:
            mido.set_backend(name=backend, load=load)

            DeviceManager()
            # Load the default output for when device_ids aren't provided
            inputs = DeviceManager.get_device_ids().get('inputs')
            output = mido.open_output()
            DeviceManager._device_out_ports.update({'default': output, inputs[0]: output})
        return DeviceManager.__instance

    @staticmethod
    def open_device_out_port(device_id=None):
        if device_id:
            try:

                # noinspection PyUnresolvedReferences
                device_out_port = mido.open_output(device_id)
                DeviceManager._device_out_ports.update({device_id: device_out_port})
            except Exception as e:
                print(e)
                return DeviceManager._device_out_ports.get('default')
        else:
            return DeviceManager._device_out_ports.get('default')

    @staticmethod
    def get_device_out_port(device_id='default', load_device=True):
        if not device_id in DeviceManager._device_out_ports.keys() and load_device:
            DeviceManager.open_device_out_port(device_id)
        return DeviceManager._device_out_ports.get(device_id)

    @staticmethod
    def send_midi_message(message=mido.Message, device_id=None, load_device=True):
        device_to_open = device_id
        if not device_id:
            device_to_open = 'default'
        out_port = DeviceManager.get_device_out_port(device_to_open, load_device=load_device)
        print('Sending message on device {}'.format(device_to_open))
        out_port.send(message)

    @staticmethod
    def get_device_ids():
        # noinspection PyTypeChecker
        mido_backend: Backend = mido

        return dict(
            {
                'inputs': mido_backend.get_input_names(),
                'outputs': mido_backend.get_output_names(),
                'ioports': mido_backend.get_ioport_names(),
            }
        )

    @staticmethod
    def get_output_devices():
        return DeviceManager.get_device_ids().get('outputs')

    def __init__(self):
        """Virtually private constructor."""
        if DeviceManager.__instance is not None:
            raise Exception("Singleton class can not be instantiated twice.")
        else:
            DeviceManager.__instance = self


device_manager = DeviceManager.getInstance("mido.backends.pygame", True)
