from flask import Blueprint
from flask import Blueprint, flash, render_template, request, url_for, redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/content-page.html')
def event():
    return render_template('content-page.html')

@main_bp.route('/createevent.html')
def createevent():
    return render_template('createevent.html')

@main_bp.route('/payment.html')
def payment():
    return render_template('payment.html')

@main_bp.route('/booking.html')
def bookings():
    return render_template('booking.html')

