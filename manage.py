from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Actor, Movie

from app import APP
from models import db

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()