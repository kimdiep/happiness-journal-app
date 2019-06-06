import sys
sys.path.append('../')

from app import db

class Idea(db.Model):
    __tablename__ = 'ideas'
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.String(120), unique=False, nullable=True)

    def __repr__(self):
        return '<Idea %r>' % self.note

    def __init__(self, note, complete):
        self.note = note
        self.complete = complete