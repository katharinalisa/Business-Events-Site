from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

#creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email address", validators=[InputRequired('Enter your email address')])
    password=PasswordField("Password", validators=[InputRequired('Enter password')])
    submit = SubmitField("Login")

  # this is the registration form
class RegisterForm(FlaskForm):
    firstname=StringField("First Name", validators=[InputRequired()])
    lastname=StringField("Last Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email()])
    password=PasswordField("Password", validators=[InputRequired('Enter a password')])
    phone=StringField("Phone", validators=[InputRequired()])
    submit = SubmitField("Register")
