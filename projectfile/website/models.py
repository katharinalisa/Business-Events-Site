from . import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(150), nullable=False)
    comments = db.relationship('Comment', backref='user')
    bookings = db.relationship('Booking', backref='user')
    def __repr__(self):
        return f"User: {self.firstname}"
    def get_id(self):
        return str(self.user_id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120))
    street = db.Column(db.String(100))
    suburb = db.Column(db.String(50))
    postcode = db.Column(db.Integer)
    state = db.Column(db.String(3))
    price = db.Column(db.Integer)
    date = db.Column(db.Date)
    starttime = db.Column(db.Time)
    endtime = db.Column(db.Time)
    performer = db.Column(db.String(100))
    tickets_available = db.Column(db.Integer)
    event_category = db.Column(db.String(50))
    event_type = db.Column(db.String(30))
    image = db.Column(db.LargeBinary)
    description = db.Column(db.Text)
    comments = db.Column(db.Text)
    comment_id = db.relationship('Comment', backref='event')
    booking_id = db.relationship('Booking', backref='event')
    def __repr__(self):
        return f"Event: {self.event_id} {self.event_name}"

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120))
    date_time = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
    def __repr__(self):
        return f"Comment: {self.text}"

class Booking(db.Model):
    __tablename__ = 'bookings'
    booking_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120))
    booking_datetime = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'))
