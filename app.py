from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, User, Note
import os

engine = create_engine('sqlite:///Notes.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/Notes/')
def notes():
    notes = session.query(Note).all()
    return render_template('Notes.html', notes=notes)

@app.route('/Notes/JSON/')
def NotesJSON():
    notes = session.query(Note).all()
    return jsonify(RestaurantNames = [i.serialize() for i in notes])

@app.route('/Notes/New/', methods=['GET', 'POST'])
def newNote():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        Note1 = Note(title=title, content=content)
        session.add(Note1)
        session.commit()
        return redirect(url_for('notes'))

    return render_template('new_note.html')

@app.route('/Notes/<int:note_id>/Page/')
def page(note_id):
    note = session.query(Note).filter_by(id=note_id).one()
    return render_template('Page.html', note=note)

@app.route('/Notes/<int:note_id>/delete', methods = ['GET', 'POST'])
def delete(note_id):
    itemToDelete = session.query(Note).filter_by(id=note_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash("Item Deleted!", 'success')
        return redirect(url_for('notes'))
    else:
        return render_template('Page.html', item=itemToDelete)
