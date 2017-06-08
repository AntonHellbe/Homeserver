from wtforms import BooleanField, StringField, PasswordField, validators
from flask_wtf import FlaskForm
from .models import User

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.Required()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I Accept the Terms of Service...blablablabla', [validators.Required()])


class EditForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')

    def __init__(self, original_username, original_email, *args, **kwargs):
        FlaskForm.__init__(self, *args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        if self.username.data == self.original_username and self.email.data == self.original_email:
            return True
        user = User.query.filter_by(username = self.username.data).first()
        if user != None:
            self.username.errors.append('Username already taken, choose another one')
            return False
        user = User.query.filter_by(email = self.email.data).first()
        if user != None:
            self.email.errors.append('Email already taken, choose another one')
            return False
        return True
