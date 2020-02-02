import json
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

with open("actualInfo.json",'r') as j:
    posts = json.load(j)

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/data")
def data():
    return render_template("data.html", posts=posts[0]["listings"], dates=posts[0]["dates"])

if __name__ == "__main__":
    app.run(debug=True)