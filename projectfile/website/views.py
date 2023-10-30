from flask import Blueprint
from flask import Blueprint, flash, render_template, request, url_for, redirect
from .models import Event
from datetime import datetime, timedelta

# Blueprint for main routes handling different pages of the web application.
# Each route renders a specific HTML template when accessed.

main_bp = Blueprint('main', __name__)

# Route for the home page (index).
@main_bp.route('/')
def index():
    current_date = datetime.now().date()  # Get the current date
    events = Event.query.all()
    max_acceptable_date = current_date + timedelta(days=7)
    events = Event.query.all()
    filtered_events = [event for event in events if current_date <= event.date <= max_acceptable_date]
    return render_template('index.html', events=events, filtered_events=filtered_events)
    
# Route for the event content page.
@main_bp.route('/content-page.html')
def event():
    return render_template('content-page.html')
    
# Route for the event creation page.
@main_bp.route('/createevent.html')
def createevent():
    return render_template('createevent.html')
    
# Route for the payment page
@main_bp.route('/payment.html')
def payment():
    return render_template('payment.html')
    
# Route for the booking page.
@main_bp.route('/booking.html')
def bookings():
    return render_template('booking.html')

