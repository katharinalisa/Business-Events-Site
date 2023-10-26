from flask import Blueprint, flash, render_template, request, url_for, redirect
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is the hint for a login function
@auth_bp.route('/login.html', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if a user with the provided phone number exists
        user_email = User.query.filter_by(email=email).first()

        if user_email and user_email.check_password(password):
            session['user_id'] = user_email.user_id
            login_user(user_email)
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Email and password do not match! Please try again', 'error')

    return render_template('login.html', form=login_form)

@auth_bp.route('/register.html', methods=['GET', 'POST'])
def sign_up():
    data = request.form
    print(data)
    register_form = RegisterForm()
    if request.method =='POST':
        email = register_form.email.data
        password = register_form.password.data  # Get the password directly from the form
        firstname = register_form.firstname.data
        lastname = register_form.lastname.data
        phone = register_form.phone.data
        existing_user_phone = User.query.filter_by(phone=phone).first()
        existing_user_email = User.query.filter_by(email=email).first()
    
        if len(email) < 4:
            flash('Email is too short', category='error')
        elif len(firstname) < 2:
            flash('Name should be at least 2 or morecharacters', category='error')
        elif len(lastname) < 2:
            flash('Surname should be at least 2 or more characters', category='error')
        elif len(password) < 8:
            flash('Password must be at least 8 or more characters long', category='error')
        elif len(phone) < 5:
            flash('Phone number is too short', category='error')

        elif existing_user_phone:
            flash('Phone number already exists. Please choose a different Phone number.', 'error')
        elif existing_user_email:
            flash('Email already exists. Please choose a different Phone number.', 'error')
        else:
        # Hash the password before storing it in the database
            hashed_password = generate_password_hash(password)

            # Create a new user and add it to the database
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password, phone=phone)
            db.session.add(new_user)
            db.session.commit()

            flash('Account successfully created! You can now log in.', category='success')
            return redirect(url_for('main.index'))

    return render_template('register.html', form=register_form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth_bp.route('/payment.html', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        cardholder = request.form.get('cardholder')
        cardnumber = request.form.get('cardnumber')
        expirydate = request.form.get('expirydate')
        cvv = request.form.get('cvv')