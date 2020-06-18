from flask import Flask, render_template, request, session


app = Flask(__name__)

# app.config["SESSION_PERMANENT"]= False
# app.config["SESSION_TYPE"]= "filesystem"
# Sesssion(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/hello", methods= ["GET", "POST"])
def hello():
    if request.method == "GET":
        return "please submit form instead"
    else:
        name = request.form.get("name")
        zipcode = request.form.get("zipcode")
        value =  request.form.get("value")
        return render_template("hello.html", name = name, zipcode= zipcode, value = value)

if __name__ == '__main__':
    app.debug = True
    app.run()
