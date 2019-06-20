import sys
sys.path.append('./models')

from flask_testing import TestCase
import unittest
from app import app, db
from happiness_journal import *
from user_model import User

class TestingViews(TestCase):

  # creates instance of flask app
  def create_app(self):
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///testing.db'
    return app

  # setup testing database
  def setUp(self):
    db.create_all()
    idea1 = Idea("This is a test note", complete = False)
    idea2 = Idea("This is another test note", complete = False)
    pusheen = User('pusheen','test123')
    db.session.add_all([idea1, idea2, pusheen])
    db.session.commit()
  
  def test_homepage(self):
    response = self.client.get('/', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Hello, Happiness Journal!', response.data)

  def test_view_ideas(self):
    response = self.client.get('/ideas', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Happiness Journal Ideas!', response.data)
    self.assertIn(b'This is a test note', response.data)
    self.assertIn(b'This is another test note', response.data)

  def test_create_idea(self):
    new_idea = self.client.post(
      '/ideas/new',
      data=dict(idea_note="Created a new note"),
      follow_redirects=True
    )
    self.assertIn(b'Created a new note', new_idea.data)

  def test_edit_route(self):
    response = self.client.get('/ideas/edit/2', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)

  def test_edit_idea(self):
    edit_idea = self.client.post(
      '/ideas/edit/2',
      data=dict(idea_note="This is another test note - edited"),
      follow_redirects=True
    )
    self.assertIn(b'This is another test note - edited', edit_idea.data)

  def test_delete_idea(self):
    response = self.client.get('/ideas/delete/1', content_type = 'html/text', follow_redirects=True)
    self.assertNotIn(b'This is a test note', response.data)

  def test_signup(self):
    response = self.client.get('/signup', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'username', response.data)
    self.assertIn(b'password', response.data)
    self.assertIn(b'Sign Up!', response.data)

  def test_login(self):
    response = self.client.get('/login', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'username', response.data)
    self.assertIn(b'password', response.data)
    self.assertIn(b'Log In!', response.data)

  def test_signup_new_user(self):
    new_user = self.client.post(
      '/signup',
      data=dict(username="newpusheen",password="newpusheen123"),
      follow_redirects=True
    )
    self.assertEqual(new_user.status_code, 200)

  def test_signin_existinguser(self):
    existing_user = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    self.assertEqual(existing_user.status_code, 200)
    
  def tearDown(self):
    db.drop_all()
    db.session.remove()


if __name__ == '__main__':
  unittest.main()



