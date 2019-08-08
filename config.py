import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_PORT = 465
    MAIL_DEFAULT_USER = 'no-reply@nexure.co.ke'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    CONFIRMATION_ENDPOINT = 'https://nexure.co.ke/confirm'
    LOGIN_ENDPOINT = 'https://nexure.co.ke/login'


class Production(Config):
    DEBUG = False


class Staging(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    ALLOWED_HOSTS = "*"


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000
    ALLOWED_HOSTS = "*"


class Testing(Config):
    TESTING = True
