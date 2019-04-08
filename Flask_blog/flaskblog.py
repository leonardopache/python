from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = 'f822c6f7d161d4b883ef2edd28fe498a'
posts = [
    {
        'author':'Leonardo pache',
        'title':'Blog Post one',
        'content':'First blog post content',
        'date_posted':'April 04, 2019'
    },
    {
        'author':'Arya stark',
        'title':'Blog Post two',
        'content':'Second blog post content',
        'date_posted':'April 01, 2019'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)


@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for { form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=form)
