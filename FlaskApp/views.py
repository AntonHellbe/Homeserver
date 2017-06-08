from . import app, db, lm
from flask import render_template, redirect, flash, url_for, request, g, session
from flask_login import login_user, logout_user, current_user, login_required
from .models import User
from .forms import LoginForm, RegistrationForm, EditForm



# @app.before_first_request
# def create_db():
#     db.create_all()
    # user1 = User(username="Anton2", email = "antonhellbe2@gmail.com")
    # user1.set_password("fabrik22")
    # db.session.add(user1)
    # db.session.commit()


    # admin_role = Role(name='Admin')
    # db.session.add(admin_role)
    # db.session.commit()
    # mod_role = Role(name='Moderator')
    # db.session.add(mod_role)
    # db.session.commit()
    # user_role = Role(name='User')
    # db.session.add(user_role)
    # db.session.commit()
    # user1 = User(username="Anton", password="fabrik22", email = "antonhellbe@gmail.com", role_id=1)
    # db.session.add(user1)
    # db.session.commit()



@lm.user_loader
def user_loader(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/homepage/')
def homepage():
        return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    if g.user is not None:
        return render_template("dashboard.html", user = g.user)
    else:
        return render_template("dashboard.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route('/login/', methods= ["GET", "POST"])
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
                    return redirect(url_for("dashboard"))
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


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user:
            error = "Username already taken"
            return render_template('register.html', form = form, error = error)
        else:
            new_user = User(username = form.username.data, email = form.email.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('dashboard'))

    return render_template('register.html', form = form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user==None:
        return redirect(url_for('/'))
    form = EditForm(user.username, user.email)
    form.username.data = user.username
    form.email.data = user.email

    return render_template('user.html', user=user, form=form)

@app.route('/edit/', methods = ['GET', 'POST'])
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
        return redirect(url_for('edit'))
    else:
        form.username.data = g.user.username
        form.email.data = g.user.email

    return render_template('edit.html', form=form, user=user)

@app.route('/logout/')
def logout_page():
    logout_user()
    return redirect(url_for('homepage'))
