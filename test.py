import sys
sys.path.append('./models')

from flask_testing import TestCase
import unittest
from app import app, db
from happiness_journal import *

class TestingViews(TestCase):

    #creates instance of flask app
  def create_app(self):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
    return app

  def setUp(self):
    db.create_all()
    idea1 = Idea("This is a test note", complete = False)
    idea2 = Idea("This is another test note", complete = False)
    db.session.add_all([idea1, idea2])
    db.session.commit()
    
  def test_homepage(self):
    response = self.client.get('/', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Hello, Happiness Journal!', response.data)

  def test_ideas(self):
    response = self.client.get('/ideas', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Happiness Journal Ideas!', response.data)
    self.assertIn(b'This is a test note', response.data)
    self.assertIn(b'This is another test note', response.data)


  def tearDown(self):
    db.drop_all()
    db.session.remove()


if __name__ == '__main__':
  unittest.main()



