from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from bucketlist_api import db
from bucketlist_api.app import app

app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('BUCKETLIST_SETTINGS', silent=True)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
