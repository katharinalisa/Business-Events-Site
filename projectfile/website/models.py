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
    comment_id = db.relationship('Comment', backref='user')
    booking_id = db.relationship('Booking', backref='user')
    def __repr__(self):
        return f"User: {self.user_id}"
    def get_id(self):
        return str(self.user_id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Event(db.Model):
    __tablename__ = 'events'
    event_id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120))
    location = db.Column(db.String(200))
    price = db.Column(db.String(10))
    date = db.Column(db.String(50))
    time = db.Column(db.String(50))
    performer = db.Column(db.String(100))
    event_category = db.Column(db.String(50))
    event_type = db.Column(db.String(30))
    description = db.Column(db.String(2000))
