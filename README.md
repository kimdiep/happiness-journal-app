# happiness-journal-app

This is my personal project to create a Happiness Journal App using Flask and SQLAlchemy. The Happiness Journal is a place for noting down ideas for self-care and notes on everything awesome! (｡◕ ‿ ◕｡)

## Features

Users can:

- Sign up to the Happiness Journal App
- If existing user, they can sign into the Happiness Journal App
- Add ideas for self-care and awesome notes (entries) with a date and text
- Create, view, update and delete their entries

## Motivation: What are my goals for this project?

I want to learn more about:

- Python
- CRUD (create, read, update, delete)
- Flask
- Flask testing
- Jinja2 templating engine
- OAuth with Flask
- PostgreSQL
- SQLAlchemy ORM
- Postman

## Build status

[![Build Status](https://travis-ci.org/kimdiep/happiness-journal-app.svg?branch=master)](https://travis-ci.org/kimdiep/happiness-journal-app)

## Code style

## Screenshots

## Tech/framework used

- Python
- Flask
- Jinja2 templating engine
- OAuth
- PostgreSQL
- SQLAlchemy ORM
- Postman

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
https://www.sqlalchemy.org/

- psycopg2-binary
Psycopg is the most popular PostgreSQL database adapter for the Python programming language.

## Code Example

## Getting started/Installation

`git clone https://github.com/kimdiep/happiness-journal-app.git`

```bash
pip3 install -r requirements.txt # to install python dependencies
```

Ensure postgresql is installed, on macOS:
`brew install postgresql`

- Postman
Go to this link to install Postman:
https://www.getpostman.com/downloads/


## How to use?

To start up the Flask server:

`python3 app.py`

Alternatively, you can also tell your terminal the application to work with by exporting the FLASK_APP environment variable and setting the debug mode to `true` to enable the server to detect changes:

```bash
$ export FLASK_APP=app.py
$ export FLASK_DEBUG=1
$ flask run
 * Running on http://127.0.0.1:5000/
```


### Creating a database and database tables in psql using SQLAlchemy

1. Enter `psql` to connect to the database server
2. `CREATE DATABASE "happiness-journal";` will create a database for the happiness journal
3. `\l` to list database to ensure `happiness-journal` is a database, `\q` to quit psql server

### Database Migrations with Flask Migrate

**Option 1 (personal project):**

`db.create_all` to create db tables in Flask-SQLAlchemy

 In the root directory, start `python3` and enter the following commands to initialise database tables from the `happiness-journal.py` SQLAlchemy model:

```python

>>> from main import db
>>> db.create_all()
>>> exit()

```

**Option 2 (collaborative working):**
- To track changes in db schema
- Import 'Migrate' class from 'flask_migrate'. Pass 'Migrate' to app along with db instance.
- Change to the structure of the database should be recorded in a migration

1. Setup migration repository from root of project directory (you only need to do this once):

```bash
`flask db init`
```

2. Run `flask db migrate` or with a message `flask db migrate -m "creates ideas table"` to create pending migrations based on the model `happiness_journal.py'
This will create a file within `/migrations/versions`

3. To run the migration file, type `flask db upgrade`. It will run SQL to make a change to the db schema and moves forward with pending migrations

4. To go back in the migration history, do `flask db downgrade`


**unittest and flask-testing**
Unit tests for routes and test database using flask-testing module.

Tests are available in `test.py`. To run the tests:

```bash

python3 test.py -v

```

## Troubleshooting

### Python 3.8+
For the latest Python versions 3.8+, you may get the error while installing Python dependencies.

```bash
pip3 install -r requirements.txt # to install python dependencies

```

```bash
ImportError: cannot import name 'url_encode' from 'werkzeug
```

You can fix this by setting  `werkzeug==1.0.0` to `werkzeug==0.16.1`

https://stackoverflow.com/questions/60896993/importerror-cannot-import-name-url-encode-from-werkzeug


## Credits

## License

MIT © 2019 thekimmykola (Kim Diep)