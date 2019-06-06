import sys
sys.path.append('./models')

from flask import Flask, request, jsonify, render_template
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

app = Flask(__name__)

@app.route('/')
def index():
  text = "Hello, Happiness Journal!"
  return render_template('index.html', message = text)

@app.route('/ideas')
def ideas():
  text = "My Happiness Journal Ideas!"
  return render_template('ideas/homepage.html', message = text)


if __name__=="__main__":
  app.run(debug=True)