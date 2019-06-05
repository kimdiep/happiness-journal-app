from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
  text = "Hello, Happiness Journal!"
  return render_template('index.html', message = text)

@app.route('/ideas')
def ideas():
  text = "My Happiness Journal Ideas!"
  return render_template('ideas/homepage.html', message = text)


if __name__=="__main__":
  app.run(debug=True)