from flask import *
import feedparser
from bs4 import BeautifulSoup
from functools import *

app = Flask(__name__)

app.secret_key = "cats"

@app.route('/')
def home():
    return render_template('home.html')

def login_required(test): #funkcja sprawdza status zalogowania
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
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            error ='wrong login or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('wykop'))
    return render_template('log.html', error=error)

@app.route('/wykop')
@login_required #sprawdzenie zalogowania
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
