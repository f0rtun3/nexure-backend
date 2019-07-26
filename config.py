import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    MAIL_SERVER = 'smtp.mail.us-east-1.awsapps.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'no-reply@nexure.co.ke'
    MAIL_PASSWORD = os.environ['EMAIL_PASSWORD']
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
