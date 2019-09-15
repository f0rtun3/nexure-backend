import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import db, application
from models import *

application.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(application, db)
manager = Manager(application)


manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host=application.config['HOST'], port=application.config['PORT']))


if __name__ == '__main__':
    manager.run()
