from flask import Flask, render_template

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ba915d57002566be361a533bf01ea64f'

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
    return render_template('about.html', title = 'About')

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login")
def register():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form = form)

if __name__ == "__main__":
    app.run(debug = True)