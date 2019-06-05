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
- OAuth with Flask
- PostgreSQL
- SQLAlchemy
- Postman

## Build status

[![Build Status](https://travis-ci.org/kimdiep/happiness-journal-app.svg?branch=master)](https://travis-ci.org/kimdiep/happiness-journal-app)

## Code style

## Screenshots

## Tech/framework used

- Python
- Flask
- OAuth
- PostgreSQL
- SQLAlchemy
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

To start up the Flask app:

`python3 main.py`

Alternatively, you can also tell your terminal the application to work with by exporting the FLASK_APP environment variable:

```bash
$ export FLASK_APP=app.py
$ flask run
 * Running on http://127.0.0.1:5000/
```

**unittest and flask-testing**
Unit tests for routes and test database using flask-testing module.

Tests are available in `test.py`. To run the tests:

```bash

python3 test.py -v

```

## Credits

## License

MIT © 2019 thekimmykola (Kim Diep)