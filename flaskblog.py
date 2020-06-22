from flask import Flask, render_template, url_for
app = Flask(__name__)

posts = [
    ## a [list] of {dictionaries}, where each dictionary=1 blog post
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'John Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]

@app.route("/")
@app.route("/home") 
##means .com/ and .com/home both lead to this page
def home():
    return render_template('home.html', posts=posts)  

@app.route("/about")
def about():
    return render_template('about.html', title='About')
 
if __name__=='__main__':
    app.run(debug=True)

#having issues running? cd, export FLASK_APP = flaskblog . py, then use flask run