import sys
sys.path.append('./models')

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker
from flask_modus import Modus
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/happiness-journal'
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)

from happiness_journal import *

def create_session(config):
    engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
    Session = sessionmaker(bind=engine)
    session = Session()
    session._model_changes = {}
    return session

manual_session = create_session(app.config)

@app.route('/')
def index():
  text = "Hello, Happiness Journal!"
  return render_template('index.html', message = text)

@app.route('/ideas', methods=["GET", "POST"])
def ideas():
  text = "My Happiness Journal Ideas!"
  if request.method == 'POST':
    new_idea = Idea(note=request.form['idea_note'], complete=False)
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('ideas'))
  return render_template('ideas/homepage.html', message = text, ideas = Idea.query.all())

@app.route('/ideas/edit/<int:id>', methods=["GET", "POST"])
def edit(id):
  idea = Idea.query.get(id)
  if request.method == 'POST':
    idea.note = request.form['idea_note']
    db.session.commit()
    return redirect(url_for('ideas'))
  return render_template('ideas/edit.html', idea = idea)

@app.route('/ideas/delete/<int:id>', methods=['GET'])
def delete(id):
  idea = Idea.query.get(id)
  db.session.delete(idea)
  db.session.commit()
  
  return redirect(url_for('ideas'))


if __name__=="__main__":
  app.run(debug=True)