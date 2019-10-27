# File to create the bon-APP-etit website
from flask import Flask, render_template, request
import pymysql

app = Flask(__name__)

@app.route('/')
def home():
  return render_template('pref.html')

@app.route('/home/', methods=['POST'])
def generateRecipes():
  budget = request.form['budget']
  service = request.form['service']
  prep_time = request.form['prep_time']
  table = queryForRecipes(budget, service, prep_time)
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  recipes = []
  for i in range(0,7):
    if i < len(table):
      recipes += [days[i], table[i]]
    else:
      recipes += [days[i], table[i % len(table)]]

  print(recipes)

  return render_template('home.html', table=recipes)

def queryForRecipes(budget, service, prep_time):
  db = pymysql.connect(host="sdhacks.cvy5vzbkf5qv.us-west-1.rds.amazonaws.com", port=3306, user="admin", passwd="Bajamk0127", db="sdhacks")
  cursor = db.cursor()

  sql = """SELECT recipe, image, url, prep_time, servings, cost from sdhacks.RECIPE where servings = """+str(service)+""" and cost <= """+str(int(budget)/7)+""" and prep_time <= """+str(prep_time)+""" LIMIT 7"""

  cursor.execute(sql)

  return cursor.fetchall()

if __name__ == '__main__':
  app.run()
