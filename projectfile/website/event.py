from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment
from .forms import EventForm, CommentForm
from . import db
from flask import Flask, flash, redirect, render_template, request, url_for
from datetime import datetime
import sqlalchemy.exc
from flask_login import LoginManager
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

  # Flask Blueprint for Event Routes
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
        price = form.price.data  # Assuming price is a float column
        date_str = form.date.data
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        starttime_str = form.starttime.data  # Assuming it's in the format 'HH:MM'
        endtime_str = form.endtime.data
        starttime = datetime.strptime(starttime_str, '%H:%M').time()
        endtime = datetime.strptime(endtime_str, '%H:%M').time()
        performer = form.performer.data
        event_category = form.event_category.data
        event_type = form.event_type.data
        description = form.description.data
        comments = form.comments.data
        image = db_file_path

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
                comments=comments,
                image=image
            )

            db.session.add(new_event)
            db.session.commit()
            flash('Successfully created a new event!', 'success')
            return redirect(url_for('event.create'))
        
    return render_template('createevent.html', form=form)



def check_upload_file(form):
    fp = form.image.data
    if fp is not None:
        filename = fp.filename
        BASE_PATH = os.path.dirname(__file__)
        upload_path = os.path.join(BASE_PATH, 'static/images', secure_filename(filename))
        db_upload_path = '/static/images/' + secure_filename(filename)
        fp.save(upload_path)
        return db_upload_path
    else:
        return None

@destbp.route('/<event_id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(event_id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, destination=destination,
                        user=current_user) 

      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', event_id=event_id))
