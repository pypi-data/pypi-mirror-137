from flask import Flask
from flask_debugtoolbar import DebugToolbar, DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SECRET'})
app.debug = False
toolbar = DebugToolbarExtension(app)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
db.session.expire_on_commit = False

# noinspection PyPep8
import twidi.admin.main
