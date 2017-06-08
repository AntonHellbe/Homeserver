from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



app = Flask(__name__)
app.config.from_envvar('FLASK_CONFIG')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////sqlite/testing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = 'super-mega-secretkey123456789'
app.config['SECRET_KEY'] = 'abc123456789fghjklmnopqwet1231543rmkadmsa'
app.config['SECURITY_REGISTERABLE'] = True
lm = LoginManager()
# app.config.from_object('config')
db = SQLAlchemy(app)
lm.init_app(app)
lm.login_view = 'login_page'
Bootstrap(app)

from FlaskApp import views, models
