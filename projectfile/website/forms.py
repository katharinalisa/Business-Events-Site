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
    
  class CommentForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired()])
    submit = SubmitField('Create')
    
  # this is the event form
class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    date = StringField("Date", validators=[InputRequired()])
    time = StringField("Time", validators=[InputRequired()])
    performer = StringField("Performer", validators=[InputRequired()])
    image = FileField('Destination Image', validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    event_category = StringField("Event category", validators=[InputRequired()])
    event_type = StringField("Event type", validators=[InputRequired()])
    description = StringField("Description", validators=[InputRequired()])
    comment_id = StringField("Comment", validators=[InputRequired()])
    submit = SubmitField('Create Event')


    class BookingForm(FlaskForm):
        booking_ref=StringField("First Name", validators=[InputRequired()])
        event_name=StringField("Last Name", validators=[InputRequired()])
        booking_datetime = StringField("Email Address", validators=[Email()])
        password=PasswordField("Password", validators=[InputRequired(message='Enter a password')])
    
