from flask import Flask, render_template
app=Flask(__name__)

posts = [
    {
        'author': 'Taylor Swift',
        'title': '1989',
        'content': '6th album released',
        'date_posted': 'Not sure'
    },
    { 
        'author': 'Taylor Swift',
        'title': 'Red',
        'content': '4th album released',
        'date_posted': 'Sometime in 2015'
        }
]
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__=='__main__':
    app.run(debug=True)