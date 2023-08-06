from flask import Response, request
from flask_admin import expose, BaseView

# Flask and Flask-SQLAlchemy initialization here
from jinja2 import Markup

from twidi.admin import app
from twidi.admin.models import ControlMessage, Device, NoteMessage, Command, MidiMessage
from twidi.twitch.midi_bot import MidiInterface


class DebugView(BaseView):
    @expose("/")
    def index(self):
        devices = self.get_devices()
        device_with_commands = []
        for device in devices:
            device_with_commands.append({'device': device, 'commands': self.get_commands_for_device(device=device)})

        return self.render(
            "debug.html", data={'devices': device_with_commands}
        )

    def __init__(self, session, **kwargs):
        super().__init__(**kwargs)
        self.session = session

    # Database-related API
    def get_query(self, model=None):
        """
        Return a query for the model type.

        This method can be used to set a "persistent filter" on an index_view.

        Example::

            class MyView(ModelView):
                def get_query(self):
                    return super(MyView, self).get_query().filter(User.username == current_user.username)


        If you override this method, don't forget to also override `get_count_query`, for displaying the correct
        item count in the list view, and `get_one`, which is used when retrieving records for the edit view.
        """
        return self.session.query(self.model if not model else model)

    def get_commands_for_device(self, device: Device = None):
        return_value = []
        return_value.extend(self.get_query(model=ControlMessage).filter(Device.device_id == device.device_id).all())
        return_value.extend(self.get_query(model=NoteMessage).filter(Device.device_id == device.device_id).all())
        return return_value

    @app.route('admin/debug/test_message', methods=['POST'])
    def test_midi_message(self):
        if request.method == 'POST':
            message_id = request.args.get('id')
            dict_copy = dict(request.form)
            device_id = None

            message = None
            if request.args.get('type') == 'control_change':
                if 'device' in dict_copy.keys():
                    device_id = int(dict_copy.pop('device'))
                    device = self.session.query(Device).filter(Device.id == device_id).first()
                    dict_copy.update({'device': device})
                if 'channel' in dict_copy.keys():
                    dict_copy['channel'] = int(dict_copy['channel'])
                if 'value' in dict_copy.keys():
                    dict_copy['value'] = int(dict_copy['value'])
                if 'cc_number' in dict_copy.keys():
                    dict_copy['cc_number'] = int(dict_copy['cc_number'])
                message = ControlMessage(**dict_copy)
            try:
                if message:
                    MidiInterface().send_midi_message(message, value=request.form.get('value'))
            except Exception as e:
                print(e)

            return Response(status=200, response=message.__repr__() if message else '')

    def get_devices(self):
        return self.get_query(model=Device).all()

    def test_message(self, model):
        # render a form with a submit button for student, include a hidden field for the student id
        # note how checkout_view method is exposed as a route below

        _html = """
            <form action="test_message" method="POST">
                <input id="student_id" name="student_id"  type="hidden" value="{student_id}">
                <button type='submit'>Send Message</button>
            </form
        """.format(
            checkout_url="", student_id=model.id
        )

        return Markup(_html)

    column_list = (
        ControlMessage.label,
        ControlMessage.value,
        ControlMessage.cc_number,
        ControlMessage.channel,
        "id",
    )
    column_formatters = {
        "id": test_message,
    }

    list_template = "admin/model/list.html"
