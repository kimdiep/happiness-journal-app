import sys
sys.path.append('../')

from app import db

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(120), unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Idea %r>' % self.note

    def __init__(self, note, complete, user_id):
        self.note = note
        self.complete = complete
        self.user_id = user_id