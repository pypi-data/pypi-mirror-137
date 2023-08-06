# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
import os.path

FLASK_ADMIN_SWATCH = 'cerulean'

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
DEV_DATABASE = 'sqlite+pysqlite:///:memory:'

dir = os.path.dirname(__file__)
VERSION = 'v0.0.0'
DATABASE_FILE = os.path.join(dir, VERSION + '_Twidi.sqlite')
DEV_SQLALCHEMY_DATABASE_URI = DEV_DATABASE
PROD_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_DATABASE_URI = PROD_SQLALCHEMY_DATABASE_URI
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
