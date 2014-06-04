from flask import *
import feedparser
from bs4 import BeautifulSoup
from functools import *
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from database import db_session
from models import User

app = Flask(__name__)

app.secret_key = "cats"

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('log'))
    return render_template('register.html', form=form)

@app.route('/')
def home():
    return render_template('home.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('Login first')
            return redirect(url_for('log'))
    return wrap
 
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Logged out')
    return redirect(url_for('log'))

@app.route('/log', methods=['GET', 'POST'])
def log(): #Funkcja musi sprawdzać czy podane dane użytkownika znajdują się w bazie danych
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error ='wrong login or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('wykop'))
    return render_template('log.html', error=error)

@app.route('/wykop')
@login_required
def wykop():
    """
    Render view with ten news from wykop.
    """
    feed = feedparser.parse('http://www.wykop.pl/rss/')
    data = []
    for entry in feed['entries'][:10]:
        img = BeautifulSoup(entry['summary']).img
        data.append({
                'link' : entry['link'],
                'title': entry['title'],
                'summary': entry['summary'],
                'published': entry['published']
                })
    return render_template('feed.html', data=data)
    
if __name__ == '__main__':
    app.run(debug=True)
