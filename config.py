import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'Jsv0#XY^ri'
    JWT_SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'oderapaul7@gmail.com'
    MAIL_PASSWORD = 'Sept21@1995'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True


class Production(Config):
    DEBUG = False


class Staging(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    ALLOWED_HOSTS = "*"
    CONFIRMATION_ENDPOINT = "https://nexure-react.herokuapp.com/confirm"


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    ALLOWED_HOSTS = "*"
    CONFIRMATION_ENDPOINT = "https://nexure-react.herokuapp.com/confirm"


class Testing(Config):
    TESTING = True
