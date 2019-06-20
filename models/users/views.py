import sys
sys.path.append('../../')

from flask import redirect, render_template, request, url_for, Blueprint
from models.users.forms import UserForm
from models.users.user_model import User
from app import db

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
  'users',
  __name__,
  template_folder='/templates/users'
)

@users_blueprint.route('/signup', methods =["GET", "POST"])
def signup():
  form = UserForm(request.form)
  if request.method == "POST" and form.validate():
    try:
      new_user = User(form.data['username'], form.data['password'])
      db.session.add(new_user)
      db.session.commit()
    except IntegrityError as e:
      return render_template('/templates/users/signup.html', form=form)
      return redirect(url_for('users.login'))
  return render_template('/templates/users/signup.html', form=form)


@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
  form = UserForm(request.form)
  if request.method == "POST" and form.validate():
    if User.authenticate(form.data['username'], form.data['password']):
      return redirect(url_for('users.welcome'))
    return render_template('/templates/users/login.html', form=form)

@users_blueprint.route('/welcome')
def welcome():
  return render_template('/templates/users/welcome.html')