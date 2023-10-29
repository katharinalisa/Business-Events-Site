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

destbp = Blueprint('event', __name__)

@destbp.route('/<event_id>', methods=['GET', 'POST'])
def show(event_id):
    event = db.session.scalar(db.select(Event).where(Event.event_id==event_id))
    form = CommentForm()    
    return render_template('content-page.html', event=event, form=form)

@destbp.route('/createevent.html', methods=['GET', 'POST'])
@login_required
@login_required
def create():
    form = EventForm()
    if form.validate_on_submit():
        try:
            # Attempt to insert data into the database
            db_file_path = check_upload_file(form)
            event = Event(
                event_name=form.event_name.data,
                street=form.street.data,
                suburb=form.suburb.data,
                postcode=form.postcode.data,
                state=form.state.data,
                price=form.price.data,
                date=datetime.strptime(form.date.data, '%Y-%m-%d'),
                starttime=datetime.strptime(form.starttime.data, '%H:%M'),
                endtime=datetime.strptime(form.endtime.data, '%H:%M'),
                performer=form.performer.data,
                event_category=form.event_category.data,
