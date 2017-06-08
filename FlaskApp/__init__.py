from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
lm = LoginManager()

#FLASK_CONFIG = C:\Users\Anton\Documents\Homeserver\Homeserver\config.py


app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
lm.init_app(app)
lm.login_view = 'login_page'
db = SQLAlchemy(app)
Bootstrap(app)

from FlaskApp import views, models
