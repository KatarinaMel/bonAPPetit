# File to create the bon-APP-etit website
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('pref.html')
    
if __name__ == '__main__':
  app.run(debug=True)
