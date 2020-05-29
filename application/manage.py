from flask_script import Manager

from apps import (create_app)
from src.config import app_config

application = create_app(app_config)

manager = Manager(application)


@manager.command
def runserver():
    application.run(host='0.0.0.0', port='8080', debug=True)


if __name__ == '__main__':
    manager.run()
