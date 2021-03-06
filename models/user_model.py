import sys
sys.path.append('../')

from app import db, bcrypt

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.Text, unique=True)
  password = db.Column(db.Text)
  idea = db.relationship('Idea', backref='user', lazy='dynamic')
  
  def __init__(self, username, password):
    self.username = username
    self.password = bcrypt.generate_password_hash(password).decode('UTF-8')