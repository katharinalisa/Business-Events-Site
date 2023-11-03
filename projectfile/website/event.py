from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Booking
from .forms import EventForm, CommentForm, BookingForm
from . import db
from datetime import datetime
import sqlalchemy.exc
from flask_login import LoginManager
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import base64
from flask import session
from secrets import token_hex

destbp = Blueprint('event', __name__)
current_date = datetime.now().date()

@destbp.route('/content-page')
def content():
    event_id = request.args.get('event_id')
    event = Event.query.get(event_id)
    comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_time.desc()).all()
    comment_form = CommentForm()
    return render_template('content-page.html', event=event, event_id=event_id)


@destbp.route('/content-page.html', methods=['GET', 'POST'])
@login_required
def comment():
    event_id = request.args.get('event_id')

    if event_id:
        event = Event.query.get(event_id)
        if event.canceled:
                flash('This event is canceled. Comments are not allowed.', 'error')
                return redirect(url_for('event.content', event_id=event_id))
            
        comments = Comment.query.filter_by(event_id=event_id).order_by(Comment.date_time.desc()).all()
        comment_form = CommentForm()
            
            if current_user.is_authenticated:
                text = comment_form.text.data  # Define text here
                if text.strip() and len(text) >= 2:
                        author_id = current_user.user_id
                        new_comment = Comment(text=text, user_id=author_id, event_id=event_id)
                        db.session.add(new_comment)
                        db.session.commit()
                        print(comments)
                        flash('Your comment has been added', 'success')
                    else:
                        flash('Comment cannot be empty or is too short', 'error')
                        return redirect(url_for('event.comment', event_id=event_id))
                else:
                    flash('Please log in', 'error')
                return render_template('content-page.html', event=event, comments=comments, comment_form=comment_form, event_id=event_id)
            else:
                flash('The event does not exist', category='error')
                return render_template('index.html')  
                
        return render_template('content-page.html', event=event, comments=comments, comment_form=comment_form, event_id=event_id)


@destbp.route('/event/cancel/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = Event.query.get(event_id)

    if event is None:
        flash('Event not found', 'error')
        return redirect(url_for('main.index'))

     if event.user_id == current_user.user_id:
            event.canceled = True  # Mark the event as canceled
            db.session.commit()
            flash('Event has been canceled', 'success')
            return render_template('content-page.html', event=event, event_id=event_id)
    else:
        flash('An error occured while canceling the event.', 'error')
    
    return redirect(url_for('main.index'))


   



@destbp.route('/createevent.html', methods=['GET', 'POST'])
@login_required
def create():
    form = EventForm()
    if request.method == 'POST':
        db_file_path = check_upload_file(form)
        event_name = form.event_name.data
        street = form.street.data
        suburb = form.suburb.data
        postcode = form.postcode.data
        state = form.state.data
        price = form.price.data 
        date_str = form.date.data
        starttime_str = form.starttime.data 
        endtime_str = form.endtime.data
        performer = form.performer.data
        event_category = form.event_category.data
        event_type = form.event_type.data
        description = form.description.data
        user_id = current_user.user_id

        if len(event_name) < 4:
            flash('Event name is too short', category='error')
        else:
            new_event = Event(
                event_name=event_name,
                street=street,
                suburb=suburb,
                postcode=postcode,
                state=state,
                price=price,
                date=date,
                starttime=starttime,
                endtime=endtime,
                performer=performer,
                event_category=event_category,
                event_type=event_type,
                description=description,
                image=db_file_path,
                user_id=user_id
            )

            db.session.add(new_event)
            db.session.commit()
            flash('Successfully created a new event!', 'success')
            return redirect(url_for('event.create'))
        
    return render_template('createevent.html', form=form)


@destbp.route('/createevent.html/<int:event_id>', methods=['GET'])
def edit_event(event_id):
    if request.method == 'POST':
        return redirect(url_for('event.create',  event_id=event_id))
    return render_template('createevent.html')

@destbp.route('/delete-event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)




def check_upload_file(form):
    fp = form.image.data
    filename = secure_filename(fp.filename)
  #get the current path of the module file… store image file relative to this path  
    BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
    upload_path = os.path.join(BASE_PATH, 'static/images', filename)
  #store relative path in DB as image location in HTML is relative
    db_upload_path = '/static/images/' + filename
  #save the file and return the db upload path
    fp.save(upload_path)
    return db_upload_path


@destbp.route('/payment.html', methods=['GET', 'POST'])
@login_required
def payment():
    event_id = request.args.get('event_id')
    event = Event.query.get(event_id)
    events = [event]
    
    # Generate a unique booking reference
    booking_ref = token_hex(4)  # This generates an 8-character hexadecimal string
    booking_form = BookingForm(request.form)
    
    if event_id is not None:
        if request.method == 'POST':
            booking_datetime = booking_form.booking_datetime.data
            event_name = booking_form.event_name.data
            price = booking_form.price.data
            image = booking_form.image.data
                
            new_booking = Booking(
                booking_ref=booking_ref,
                booking_datetime=booking_datetime,
                event_name=event_name,
                price=price,
                image=image,
                event_id=event_id,  # Assign the event_id to the booking
                user_id=current_user.user_id  # Assign the user_id to the booking
            )

            db.session.add(new_booking)
            db.session.commit()
            flash('Thank you for your purchase! You will receive a confirmation email shortly.', 'success')
            return render_template('payment.html', event=event, events=events, booking_form=booking_form)
  
    else:    
        flash('An error occurred while proceeding to pay.', category='error')
        return redirect(url_for('404.html'))
    return render_template('payment.html', event=event, events=events, booking_form=booking_form)
#

@destbp.route('/<event_id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event_id):  
    form = CommentForm()  
    destination = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
    if form.validate_on_submit():  
      comment = Comment(text=form.text.data, destination=destination,
                        user=current_user) 
      db.session.add(comment) 
      db.session.commit() 
      flash('Your comment has been added', 'success')  
    return redirect(url_for('event.show', event_id=event_id))

@destbp.route('/payment.html', methods=['GET', 'POST'])
@login_required
def payment():
    event_id = request.args.get('event_id')
    event = Event.query.get(event_id)
    events = [event]
    booking_form = BookingForm(request.form)
    if event_id is not None:
        if request.method == 'POST':
            print("test")
            

@destbp.route('/booking.html', methods=['GET'])
def bookings():
    event_id = request.args.get('event_id')  # Get the event_id from the query parameters
    session['selected_event_id'] = event_id
    if current_user.is_authenticated:
        
         bookings = Booking.query.filter_by(user_id=current_user.user_id).all()
    else:
        # Handle the case where the user is not authenticated or logged in
        flash('Please log in to view your bookings.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('booking.html', event_id=event_id, bookings=bookings)


