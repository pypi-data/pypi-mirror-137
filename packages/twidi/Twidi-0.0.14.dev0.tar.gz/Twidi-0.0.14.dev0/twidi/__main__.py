import os
import os.path as op

from twidi.admin import app, db
# Build a sample db on the fly, if one does not exist yet.
from twidi.admin.data import create_database
from twidi.admin.models import Configuration

run_app = True
create_db = False

app_dir = op.join(op.realpath(os.path.dirname(__file__)), 'admin')
database_path = op.join(app_dir, app.config['DATABASE_FILE'])

if create_db:
    create_database(recreate=True)

if __name__ == "__main__":
    # Start app
    if run_app:
        import twidi.admin.bot

        app.run(debug=False)
