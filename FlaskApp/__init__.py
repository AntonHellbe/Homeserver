from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_moment import Moment


app = Flask(__name__)
lm = LoginManager()
moment = Moment()
bootstrap = Bootstrap()
db = SQLAlchemy()

main = Blueprint('main', __name__)
from . import views, errors


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    moment.init_app(app)
    lm.login_view = 'main.login_page'

    from . import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app
