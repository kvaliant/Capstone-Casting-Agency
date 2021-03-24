from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import APP
from models import db, Actor, Movie

migrate = Migrate(APP, db)
manager = Manager(APP)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()