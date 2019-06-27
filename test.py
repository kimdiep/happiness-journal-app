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
    # Flask-WTForms - disable validation of CSRF token as not providing one for tests
    app.config['WTF_CSRF_ENABLED'] = False
    return app

  # setup testing database
  def setUp(self):
    db.create_all()
    idea1 = Idea("This is a test note", complete = False, user_id = 1)
    idea2 = Idea("This is another test note", complete = False, user_id = 1)
    idea3 = Idea("This is a Kirby test note", complete = False, user_id = 2)
    pusheen = User('pusheen','test123')
    kirby = User('kirby','test321')
    db.session.add_all([idea1, idea2, idea3, pusheen, kirby])
    db.session.commit()

  def test_view_homepage(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    self.assertEqual(sign_in.status_code, 200)
    self.assertIn(b'Hello, Happiness Journal!', sign_in.data)
  
  def test_view_homepage_unhappy_path(self):
    response = self.client.get('/', content_type = 'html/text', follow_redirects=True)
    self.assertNotIn(b'Hello, Happiness Journal!', response.data)
    self.assertIn(b'Whoopsie! You must be logged in first to view this page!', response.data)

  def test_view_ideas_pusheen(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    response = self.client.get('/ideas', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Happiness Journal Ideas!', response.data)
    self.assertIn(b'Add new idea', response.data)
    self.assertIn(b'Logout', response.data)
    self.assertIn(b'This is a test note', response.data)
    self.assertIn(b'This is another test note', response.data)
    self.assertNotIn(b"This is a Kirby test note", response.data)

  def test_view_ideas_kirby(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="kirby",password="test321"),
      follow_redirects=True
    )
    response = self.client.get('/ideas', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Happiness Journal Ideas!', response.data)
    self.assertNotIn(b'This is a test note', response.data)
    self.assertNotIn(b'This is another test note', response.data)
    self.assertIn(b"This is a Kirby test note", response.data)

  def test_view_ideas_unhappy_path(self):
    response = self.client.get('/ideas', content_type = 'html/text', follow_redirects=True)
    self.assertNotIn(b'Happiness Journal Ideas!', response.data)
    self.assertIn(b'Whoopsie! You must be logged in first to view this page!', response.data)

  def test_create_idea(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    new_idea = self.client.post(
      '/ideas/new',
      data=dict(idea_note="Created a new note"),
      follow_redirects=True
    )
    self.assertIn(b'Created a new note', new_idea.data)

  def test_create_ideas_unhappy_path(self):
    new_idea = self.client.post(
      '/ideas/new',
      data=dict(idea_note="Created a new note"),
      follow_redirects=True
    )
    self.assertNotIn(b'Created a new note', new_idea.data)
    self.assertIn(b'Whoopsie! You must be logged in first to view this page!', new_idea.data)

  def test_edit_route(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    response = self.client.get('/ideas/edit/2', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)

  def test_edit_route_unhappy_path(self):
    response = self.client.get('/ideas/edit/2', content_type = 'html/text', follow_redirects=True)
    self.assertIn(b'Whoopsie! You must be logged in first to view this page!', response.data)

  def test_edit_idea(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    edit_idea = self.client.post(
      '/ideas/edit/2',
      data=dict(idea_note="This is another test note - edited"),
      follow_redirects=True
    )
    self.assertIn(b'This is another test note - edited', edit_idea.data)

  def test_edit_idea_unhappy_path(self):
    edit_idea = self.client.post(
      '/ideas/edit/2',
      data=dict(idea_note="This is another test note - edited"),
      follow_redirects=True
    )
    self.assertNotIn(b'This is another test note - edited', edit_idea.data)
    self.assertIn(b'Whoopsie! You must be logged in first to view this page!', edit_idea.data)

  def test_delete_idea(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    response = self.client.get('/ideas/delete/1', content_type = 'html/text', follow_redirects=True)
    self.assertNotIn(b'This is a test note', response.data)

  def test_view_signup(self):
    response = self.client.get('/signup', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'username', response.data)
    self.assertIn(b'password', response.data)
    self.assertIn(b'Sign Up!', response.data)

  def test_signup_new_user_happy_path(self):
    new_user = self.client.post(
      '/signup',
      data=dict(username="newpusheen",password="newpusheen123"),
      follow_redirects=True
    )
    self.assertEqual(new_user.status_code, 200)
    self.assertIn(b'Log In!', new_user.data)

  def test_signup_new_user_unhappy_path(self):
    new_user = self.client.post(
      '/signup',
      data=dict(username="pusheen",password="pusheen123"),
      follow_redirects=True
    )
    self.assertEqual(new_user.status_code, 200)
    self.assertNotIn(b'Log In!', new_user.data)
    self.assertIn(b'Oopsy! Please try again!', new_user.data)

  def test_view_login(self):
    response = self.client.get('/login', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'username', response.data)
    self.assertIn(b'password', response.data)
    self.assertIn(b'Log In!', response.data)

  def test_login_existing_user_happy_path(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    self.assertEqual(sign_in.status_code, 200)
    self.assertIn(b'Woohoo! You are inside the Happiness Journal!', sign_in.data)

  def test_login_existing_user_unhappy_path(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="123"),
      follow_redirects=True
    )
    self.assertEqual(sign_in.status_code, 200)
    self.assertIn(b'Oopsy! Your username and password is unrecognised. Please try again!', sign_in.data)

  def test_logout_pusheen(self):
    sign_in = self.client.post(
      '/login',
      data=dict(username="pusheen",password="test123"),
      follow_redirects=True
    )
    response = self.client.get('/ideas', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Happiness Journal Ideas!', response.data)
    response = self.client.get('/logout', content_type = 'html/text', follow_redirects=True)
    self.assertIn(b'Goodbye! See you next time!', response.data)
    self.assertIn(b'username', response.data)
    self.assertIn(b'password', response.data)
    self.assertIn(b'Log In!', response.data)
    
  def tearDown(self):
    db.drop_all()
    db.session.remove()


if __name__ == '__main__':
  unittest.main()



