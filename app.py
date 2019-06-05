from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
  return "Hello, Happiness Journal!"

@app.route('/ideas')
def ideas():
  return "My Happiness Journal Ideas!"


if __name__=="__main__":
  app.run(debug=True)