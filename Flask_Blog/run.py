from flask import Flask, render_template

app = Flask(__name__)

posts = [
    {
        'author': 'Laurent Echeverria',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': '18 Mars 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': '19 Mars 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug = True)