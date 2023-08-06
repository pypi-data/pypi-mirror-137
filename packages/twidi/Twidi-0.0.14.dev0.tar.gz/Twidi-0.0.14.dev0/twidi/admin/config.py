# set optional bootswatch theme
# see http://bootswatch.com/3/ for available swatches
FLASK_ADMIN_SWATCH = 'cerulean'

# Create dummy secrey key so we can use sessions
SECRET_KEY = '123456790'

# Create in-memory database
DEV_DATABASE = 'sqlite+pysqlite:///:memory:'
DATABASE_FILE = 'Twidi.sqlite'
DEV_SQLALCHEMY_DATABASE_URI = DEV_DATABASE
PROD_SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_FILE
SQLALCHEMY_DATABASE_URI = PROD_SQLALCHEMY_DATABASE_URI
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
