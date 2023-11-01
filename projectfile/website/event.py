from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
from datetime import datetime
import sqlalchemy.exc
from flask_login import LoginManager
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import base64

destbp = Blueprint('event', __name__)

@destbp.route('/<event_id>', methods=['GET', 'POST'])
def show(event_id):
    event = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
    form = CommentForm()    
    return render_template('content-page.html', event=event, form=form)

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
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        starttime_str = form.starttime.data 
        endtime_str = form.endtime.data
        starttime = datetime.strptime(starttime_str, '%H:%M').time()
        endtime = datetime.strptime(endtime_str, '%H:%M').time()
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
    booking_form = BookingForm(request.form)
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
