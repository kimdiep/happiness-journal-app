import sys
sys.path.append('./models')

from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, and_, text
from sqlalchemy.orm import sessionmaker
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/happiness-journal'
modus = Modus(app)
db = SQLAlchemy(app)
Migrate(app, db)

from users.views import users_blueprint

app.register_blueprint(users_blueprint, url_prefix='/users')

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

@app.route('/ideas', methods=["GET"])
def ideas():
  text = "My Happiness Journal Ideas!"
  ideas = Idea.query.all()
  return render_template('ideas/homepage.html', message = text, ideas = ideas)

@app.route('/ideas/new', methods=['POST', 'GET'])
def new():
  if request.method == 'POST':
    new_idea = Idea(request.form['idea_note'], complete=False)
    db.session.add(new_idea)
    db.session.commit()
    return redirect(url_for('ideas'))
  return render_template('ideas/new.html')

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