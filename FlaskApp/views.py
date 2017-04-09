from . import app, db
from flask import render_template, flash, request, url_for, redirect, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from .models import User
from passlib.hash import sha256_crypt

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.Required()])

@app.route('/login/', methods= ["POST", "GET"])
def login_page():
    error = ''
    try:
    	login_form = LoginForm(request.form)
        if request.method == "POST" and login_form.validate():
			user = User.query.filter_by(username = login_form.username.data).first()
			if user:
				if user.authentication(str(login_form.password.data)):
					session['logged_in'] = True
					session['username'] = user.username
					flash("You are now logged in")
					return redirect(url_for("dashboard"))
				else:
					error = "Invalid Credentials, try again"
					return render_template("login.html", login_form=login_form, error = error)
			else:
				error = "User does not exist"
				return render_template("login.html", login_form=login_form, error = error)

        return render_template("login.html", login_form=login_form)
  
    except Exception as e:
         return render_template("login.html", error = error)
        

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I Accept the Terms of Service...blablablabla', [validators.Required()])


@app.route('/register/', methods=["GET", "POST"])
def register_page():
	error = ''
	try:
		form = RegistrationForm(request.form)
		if request.method == "POST" and form.validate():
			new_user = User.query.filter_by(username = str(form.username.data)).first()
			if new_user:
				error = "username already taken"
			else:
				new_user = User(username = form.username.data, email = form.email.data, settings = 0)
				new_user.set_password(str(form.password.data))
				db.session.add(new_user)
				db.session.commit()
				session['logged_in'] = True
				session['username'] = new_user.username
				return redirect(url_for('dashboard'))
		return render_template('register.html', form=form)

	except Exception as e:
		return render_template('register.html', error = error)

@app.route('/logout/')
def logout_page():
    session['logged_in'] = False
    flash("You have been logged out")
    return redirect(url_for('dashboard'))
