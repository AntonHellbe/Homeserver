from . import app, db, lm
from flask import render_template, redirect, flash, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Project
from .forms import LoginForm, RegistrationForm, EditForm
from . import main
from datetime import datetime



# @main.before_app_first_request
# def create_db():
#     db.create_all()
#     project1 = Project(name = "Casus", tags = "Matlab, Arduino, ESP8266", description = "Project built with Axis Camera and ESP8266", date = datetime.utcnow(), user_id = 1)
#     project2 = Project(name = "Casus1", tags = "Matlab, Arduino, ESP8266, adsadada", description = "Project built with Axis Camera and ESP8266 daldadadadasd", date = datetime.utcnow(), user_id = 1)
#     project3 = Project(name = "Casus2", tags = "Matlab, Arduino, ESP8266, abc123", description = "Project built with Axis Camera and ESP8266 aehadsadagsda", date = datetime.utcnow(), user_id = 1)
#     user1 = User(username = "AntonHellbe", email = "antonhellbe@gmail.com")
#     user1.set_password("Fabrik22")
#     db.session.add(user1)
#     db.session.add(project2)
#     db.session.add(project3)
#     db.session.commit()


@main.context_processor
def inject_moment():
    return {'now': datetime.utcnow()}

@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))

@main.before_app_request
def before_request():
    g.user = current_user

@main.route('/')
@main.route('/homepage/')
def homepage():
        return render_template("main.html")

@main.app_errorhandler(404)
def page_not_found(e):
     return render_template("404.html")


@main.route('/dashboard/')
def dashboard():
    projects = Project.query.all()
    return render_template("dashboard.html", projects = projects)


@main.route('/login/', methods= ["GET", "POST"])
def login_page():
    error = ''
    form = LoginForm()
    try:
        if form.validate_on_submit():
            user = User.query.filter_by(username = form.username.data).first()
            if user:
                if user.authentication(str(form.password.data)):
                    login_user(user)
                    flash("You are now logged in")
                    return redirect(request.args.get('next') or url_for('main.dashboard'))
                else:
                    error = "Invalid Password, try again"
                    return render_template("login.html", login_form = form, error = error)
            else:
                error = "Username does not exist"
                return render_template("login.html", login_form = form, error = error)
        return render_template("login.html", login_form = form, error = error)

    except Exception as e:
        error = "Something is wrong"
        return render_template("login.html", login_form = form, error = error)


@main.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            error = "Username already taken"
            return render_template('register.html', form = form, error = error)
        else:
            new_user = User(username = form.username.data, email = form.email.data)
            new_user.set_password(str(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            flash('Registration succesful, you are now logged in')
            return redirect(url_for('main.dashboard'))

    return render_template('register.html', form = form)

@main.route('/dashboard/project/<id>')
@login_required
def project(id):
    project = Project.query.get(id)
    return render_template('project.html', project = project)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user==None:
        return redirect(url_for('main.homepage'))
    form = EditForm(user.username, user.email)
    form.username.data = user.username
    form.email.data = user.email

    return render_template('user.html', user=user, form=form)

@main.route('/edit/', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.username, g.user.email)
    user = User.query.filter_by(username = g.user.username).first()
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data is not None:
            user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your changes have been made')
        return redirect(url_for('main.edit'))
    else:
        form.username.data = g.user.username
        form.email.data = g.user.email

    return render_template('edit.html', form=form, user=user)

@main.route('/logout/')
def logout_page():
    logout_user()
    flash('You are now logged out')
    return redirect(url_for('main.homepage'))
