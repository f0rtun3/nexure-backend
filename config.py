import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'email-smtp.us-east-1.amazonaws.com'
    MAIL_PORT = 465
    MAIL_DEFAULT_USER = 'info@nexure-plc.co.ke'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    AWS_REGION = 'us-east-1'
    AWS_REGION_S3 = 'us-east-2'
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    S3_BUCKET = os.environ['S3_BUCKET']
    S3_LOCATION = f"https://{os.environ['S3_BUCKET']}.s3.amazonaws.com/"
    CONFIRMATION_ENDPOINT = 'https://master.d2i6nspgk8q2x3.amplifyapp.com/confirm'
    LOGIN_ENDPOINT = 'https://master.d2i6nspgk8q2x3.amplifyapp.com/auth/login'
    ACCOUNT_RESET_ENDPOINT = 'https://master.d2i6nspgk8q2x3.amplifyapp.com/reset'


class Production(Config):
    DEBUG = False


class Staging(Config):
    DEVELOPMENT = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    DEBUG = True
    HOST = "127.0.0.1"
    PORT = 5000
    ALLOWED_HOSTS = "*"


class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
    HOST = "0.0.0.0"
    PORT = 5000
    ALLOWED_HOSTS = "*"


class Testing(Config):
    TESTING = True
    HOST = "127.0.0.1"
    PORT = 5000
    ALLOWED_HOSTS = "127.0.0.1"
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
