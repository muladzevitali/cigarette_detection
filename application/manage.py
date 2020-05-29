from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from apps import (create_app, database)
from apps.auth.models import User
from src.config import app_config
from src.scripts import create_users

application = create_app(app_config)
tables = [User.__table__]
migrate = Migrate(application, database, max_identifier_length=128)

manager = Manager(application)
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    with application.app_context():
        database.metadata.create_all(database.engine, tables=tables)
        create_users(User, database)


@manager.command
def reset_db():
    with application.app_context():
        database.metadata.drop_all(database.engine, tables=tables)
        create_db()


@manager.command
def runserver():
    application.run(host='0.0.0.0', port='8080', debug=True)


if __name__ == '__main__':
    manager.run()