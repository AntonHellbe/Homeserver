from . import app, db, lm
from flask import render_template, redirect, flash, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Project
from .forms import LoginForm, RegistrationForm, EditForm
from . import main



# @main.before_app_first_request
# def create_db():
#     db.create_all()
#     project1 = Project(name = "Casus", tags = "Matlab, Arduino, ESP8266", description = "Project built with Axis Camera and ESP8266")
#     db.session.add(project1)
#     db.session.commit()


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
    project = Project.query.filter_by(name = "Casus").first()
    return render_template("dashboard.html", project = project)
#    if g.user is not None:

#    else:
#        return render_template("dashboard.html")

@main.route('/login/', methods= ["GET", "POST"])
def login_page():
    error = ''
    form = LoginForm()
    try:
        if form.validate_on_submit():
            print('Step 1')
            user = User.query.filter_by(username = form.username.data).first()
            if user:
                print('Step 2')
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
            flash('Registration succesful, you are now logged in')
            return redirect(url_for('main.dashboard'))

    return render_template('register.html', form = form)

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
    return redirect(url_for('main.homepage'))
