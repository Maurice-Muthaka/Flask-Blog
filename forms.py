from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import data_required, Length, Email, EqualTo, ValidationError
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[data_required(), Length(min=3,max=20)])
    email = StringField('email',
                        validators=[data_required(), Email()])
    password = PasswordField('Password', validators=[data_required()])
    confirm_password = PasswordField('Confirm Password', validators=[data_required(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one !')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose another one !')


class LoginForm(FlaskForm):
    email = StringField('email',
                        validators=[data_required(), Email()])
    password = PasswordField('Password', validators=[data_required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[data_required(), Length(min=3,max=20)])
    email = StringField('email',
                        validators=[data_required(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one !')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose another one !')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[data_required()])
    content = TextAreaField('Content', validators=[data_required()])
    picture = FileField('Upload picture for this post', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Post')

class RequestResetForm(FlaskForm):
    email = StringField('email',
                        validators=[data_required(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account registered with this email. You have to register again')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[data_required()])
    confirm_password = PasswordField('Confirm Password', validators=[data_required(), EqualTo('password')])
    submit = SubmitField('Reset Password')