from twidi.admin import db
from twidi.admin.models import Configuration
from twidi.twitch.midi_bot import TwidiBot

c = db.session.query(Configuration).first()
bot = TwidiBot(config=c)
