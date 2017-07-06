from flask import render_template, g
from . import main
from flask_login import current_user

# @main.errorhandler(404)
# def page_not_found(e):
#     return render_template("404.html")
