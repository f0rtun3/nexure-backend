import os
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app import db, app
from models import *

app.config.from_object(os.environ['APP_SETTINGS'])
migrate = Migrate(app, db)
manager = Manager(app)


manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host=app.config['HOST'], port=app.config['PORT']))


if __name__ == '__main__':
    manager.run()
