from flask import Blueprint
from flask import Blueprint, flash, render_template, request, url_for, redirect
from .models import Event
from datetime import datetime, timedelta
from flask_login import current_user
from . import db 
from flask import Flask, jsonify

# Blueprint for main routes handling different pages of the web application.
# Each route renders a specific HTML template when accessed.

main_bp = Blueprint('main', __name__)

# Route for the home page (index).
@main_bp.route('/')
def index():
    current_date = datetime.now().date()  # Get the current date
    events = Event.query.all()
    return render_template('index.html', events=events, current_date=current_date)


@main_bp.route('/Contact Us.html')
def contact():
    return render_template('Contact Us.html')
    
@main_bp.route('/Privacy_Policy.html')
def policy():
    return render_template('Privacy_Policy.html')
    
@main_bp.route('/terms_and_conditions.html')
def terms():
    return render_template('terms_and_conditions.html')
    
# Route for the booking page.
@main_bp.route('/booking.html')
def bookings():
    return render_template('booking.html')

# Route for Forgot Password Page
@main_bp.route('/Forgot_Password.html')
def forgotpassword():
    return render_template('Forgot_Password.html')

@main_bp.route('/myevents.html')
def myevents():
    user_id = current_user.user_id 
    events = Event.query.filter_by(user_id=user_id).all()
    return render_template('myevents.html', events=events)

@main_bp.route('/Forgot_Password.html')
def forgotpassword():
    return render_template('Forgot_Password.html')

@main_bp.route('/delete_event/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    event = Event.query.get(event_id)
    if event:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully', 'success')
    else:
        flash('Event not found', 'error')
    return redirect(url_for('myevents'))
