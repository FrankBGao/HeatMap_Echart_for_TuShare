from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/visualization')
def visualization():
    data = []
    return render_template("pic.html", tree=data)


if __name__ == '__main__':
    app.run()
