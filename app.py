from flask import Flask, render_template, redirect, request
import pymongo as pymo
import algorithm.algorithm as alg
import json
app = Flask(__name__)
client = pymo.MongoClient('mongodb://localhost:27017/')
db = client['stock']

@app.route('/')
def hello_world():
    return redirect("/visualization")


@app.route('/visualization')
def visualization():
    daily, category = alg.gain_data(db)
    result = alg.gain_pic(daily, category)
    return render_template("pic.html", tree=result)

@app.route('/indus')
def indus():
    indus = request.args.get("indus")
    daily, category = alg.gain_data(db, indus)
    result = alg.gain_pic(daily, category)
    return result

@app.route('/debug')
def debug():
    return render_template("pic.html")

if __name__ == '__main__':
    app.run()
