from flask import Flask, render_template, redirect
import algorithm as alg
app = Flask(__name__)


@app.route('/')
def hello_world():
    return redirect("/visualization")


@app.route('/visualization')
def visualization():
    daily, category = alg.gain_data()
    result = alg.gain_pic(daily, category)
    return render_template("pic.html", tree=result)


if __name__ == '__main__':
    app.run()
