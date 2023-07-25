from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') # Gets the note from the HTML form

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id) # Providing the schema for the note 
            db.session.add(new_note) # Adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, notes=notes)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # This function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/update-note', methods=['POST'])
def update_note():
    note_data = json.loads(request.data) # This function expects a JSON from the INDEX.js file 
    note_id = note_data['noteId']
    new_data = note_data['newData']

    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            note.data = new_data
            db.session.commit()

    return jsonify({})
