import sys
sys.path.append('./models')

# flask setup
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
# bcrypt for password hashing
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/happiness-journal'
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)

import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# import models from happiness_journal.py for Idea
from happiness_journal import *

# generate session
def create_session(config):
  engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
  Session = sessionmaker(bind=engine)
  session = Session()
  session._model_changes = {}
  return session

manual_session = create_session(app.config)

# import form for user signup and login
# import user model
from forms import UserForm
from user_model import User

from sqlalchemy.exc import IntegrityError

# app-controllers

# homepage
@app.route('/')
def index():
  text = "Hello, Happiness Journal!"
  return render_template('index.html', message = text)

# ideas page
@app.route('/ideas', methods=["GET"])
def ideas():
  text = "My Happiness Journal Ideas!"
  ideas = Idea.query.all()
  return render_template('ideas/homepage.html', message = text, ideas = ideas)

# route to add new idea
@app.route('/ideas/new', methods=['POST', 'GET'])
def new():
  if request.method == 'POST':
    new_idea = Idea(request.form['idea_note'], complete=False)
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('ideas'))
  return render_template('ideas/new.html')

# route to edit existing idea
@app.route('/ideas/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
  idea = Idea.query.get(id)
  if request.method == 'POST':
    idea.note = request.form['idea_note']
    db.session.commit()
    return redirect(url_for('ideas'))
  return render_template('ideas/edit.html', idea = idea)

# route to delete existing idea
@app.route('/ideas/delete/<int:id>', methods=['GET'])
def delete(id):
  idea = Idea.query.get(id)
  db.session.delete(idea)
  db.session.commit()
  
  return redirect(url_for('ideas'))

# auth-route for new user to sign up
@app.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            return render_template('users/signup.html', form=form)
        return redirect(url_for('login'))
    return render_template('users/signup.html', form=form)

# auth-route for existing user to log in
@app.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        found_user = User.query.filter_by(username = form.data['username']).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, form.data['password'])
            if authenticated_user:
                return redirect(url_for('index'))
    return render_template('users/login.html', form=form)

if __name__=="__main__":
  app.run(debug=True)