from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import sys

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if note:
            if len(note) < 10:
                flash('Note is too short', category='danger')
            else:
                new_note = Note(data=note, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()
                flash('Note added', category='success')
                
        else:
            id_delete_note = request.form.get('delete_note')
            delete_note = Note.query.get(id_delete_note)
            if delete_note:
                Note.query.filter_by(id=id_delete_note).delete()
                db.session.commit()
                flash('Note deleted', category='success')
            else:
                flash('Note does not exist', category='danger')
        return redirect(url_for('views.home'))
    elif request.method == 'GET':
       return render_template('home.html', user=current_user)
