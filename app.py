from flask import Flask

app = Flask(__name__)

@app.route("/")  #accesses default place for first time
def index():  #runs this function immediately after the slash above
    return "Hello, world!!"


# @app.route("/Collins")
# def index():
#     return "Hello, Collins"

@app.route("/<string:name>")
def hello(name):
    return f"Hello, {name}!"
#export FLASK_APP= app.py
