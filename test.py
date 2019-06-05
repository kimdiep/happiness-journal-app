from flask_testing import TestCase
import unittest
from app import app

class TestingViews(TestCase):

  #creates instance of flask app
  def create_app(self):
    return app
    
  def test_homepage(self):
    response = self.client.get('/', content_type = 'html/text')
    self.assertEqual(response.status_code, 200)
    self.assertIn(b'Hello, Happiness Journal!', response.data)


if __name__ == '__main__':
  unittest.main()



