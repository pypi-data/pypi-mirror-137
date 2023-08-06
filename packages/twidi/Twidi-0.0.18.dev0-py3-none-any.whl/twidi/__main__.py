import os
import os.path as op

from twidi.admin import app, db
# Build a sample db on the fly, if one does not exist yet.
from twidi.admin.data import create_database
from twidi.admin.models import Configuration
from twidi.device.devices import device_manager

run_app = True
create_db = False

app_dir = op.join(op.realpath(os.path.dirname(__file__)), 'admin')
database_path = op.join(app_dir, app.config['DATABASE_FILE'])

if not os.path.isfile(database_path):
    create_database(recreate=True)
else:
    create_database(recreate=False)

if __name__ == "__main__":
    # Start app
    if run_app:
        import twidi.admin.bot

        ids = device_manager.get_device_ids()
        print('Use Outports for Configuration')
        print(ids)
        app.run(debug=False)
