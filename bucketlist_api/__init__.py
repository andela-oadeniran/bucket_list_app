from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.config.from_envvar('BUCKETLIST_SETTINGS', silent=True)
db = SQLAlchemy(app)
