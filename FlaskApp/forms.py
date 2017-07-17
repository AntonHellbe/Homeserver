from wtforms import BooleanField, StringField, PasswordField, FileField, ValidationError, TextAreaField, validators
from flask_wtf import FlaskForm
from .models import User, Project
from wtforms.validators import Required, Length, EqualTo, regexp
from flask_wtf.file import FileAllowed
from FlaskApp import docs
import re

class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    password = PasswordField('Password', [validators.Required()])


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[Required(), Length(4, 20)])
    email = StringField('Email Address', validators=[Length(15,64)])
    password = PasswordField('Password', [validators.Required(),
                                          validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I Accept the Terms of Service...blablablabla', [validators.Required()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already taken')

class EditForm(FlaskForm):
    username = StringField('Username', validators=[Length(4, 20)])
    email = StringField('Email Address', validators=[Length(6,50)])
    password = PasswordField('Password', validators=[EqualTo('confirm', message="passwords must match")])
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

class ProjectForm(FlaskForm):
    name = StringField('Name', validators=[Length(1, 50)])
    tags = StringField('Tags', validators=[Length(1, 200)])
    description = TextAreaField('Description', validators=[Required()])
    links = StringField('Links', validators=[Required()])
    document = FileField(u'Document file', validators=[FileAllowed(docs, 'Documents only')])

    def validate_name(self, field):
        if Project.query.filter_by(name = field.data):
            raise ValidationError('Name already taken')

class EditProjectForm(FlaskForm):
    name = StringField('Name', validators=[Length(1, 50)])
    tags = StringField('Tags', validators=[Length(1, 200)])
    description = TextFieldArea('Description', validators=[Required()])
    links = StringField('Links', validators=[Required()])
    document = FileField(u'Document file', validators=[FileAllowed(docs, 'Documents only')])

    def validate_name(self, field):
        if Project.query.filter_by(name = field.data):
            raise ValidationError('Name already taken')
    

    # def validate_document(form, field):
    #     if field.data:
    #         field.data = re.sub(r'[^a-z0-9_.-]', '_', field.data)

    def validate_name(self, field):
        if Project.query.filter_by(name = field.data).first():
            raise ValidationError('Project with this name already exists')
