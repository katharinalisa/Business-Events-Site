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
    password=PasswordField("Password", validators=[InputRequired(message='Enter a password')])
    phone=StringField("Phone")
    submit = SubmitField("Register")

class CommentForm(FlaskForm):
    text = TextAreaField('Comment')
    author = StringField('Author')
    submit = SubmitField('Create')

class EventForm(FlaskForm):
    event_name = StringField("Event Name", validators=[InputRequired()])
    street = StringField("Street", validators=[InputRequired()])
    suburb = StringField("Suburb", validators=[InputRequired()])
    postcode = StringField("Postcode", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    date = StringField("Date", validators=[InputRequired()])
    starttime = StringField("Start time", validators=[InputRequired()])
    endtime = StringField("End time", validators=[InputRequired()])
    performer = StringField("Performer", validators=[InputRequired()])
    tickets_available = StringField("Tickets available", validators=[InputRequired()])
    image = FileField("Image", validators=[
    FileRequired(message='Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports PNG, JPG, png, jpg')])
    event_category = StringField("Event category", validators=[InputRequired()])
    event_type = StringField("Event type", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    submit = SubmitField('Create Event')

class BookingForm(FlaskForm):
    booking_ref=StringField("Booking Reference", validators=[InputRequired()])
    event_name=StringField("Event Name", validators=[InputRequired()])
    booking_datetime = StringField("Booking Datetime", validators=[InputRequired()])
    price = StringField("Price", validators=[InputRequired()])
    tickets_available = StringField("Tickets available")
    image = StringField("Image", validators=[InputRequired()])
    event_id = StringField("Event ID", validators=[InputRequired()])
    submit = SubmitField("Proceed to pay")
