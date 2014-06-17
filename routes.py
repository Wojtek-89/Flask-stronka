# Dużo lepiej, mam jednak pare ale. Modeli nie trzyma się z widokam.
# bs4 jest spoko, ale dla czego zmieniles na niego z feedparsera?
# bajzel w tym programie troche
# PEP-8!!! jest do tego apka konsolowa nawet, edytory maja wbudowane sprawdzanie, poza tym
# zasady sa proste.
# nastepna misja, po kliknieciu na wybrany artykul otwiera sie on caly na Twojej stronie.
# artykuly takie zapisuj do bazy.
# przydatny lib:
# https://github.com/grangier/python-goose

from flask import *
import feedparser
from bs4 import BeautifulSoup
from functools import *
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:////tmp/test.db', echo=False)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

app = Flask(__name__)

app.secret_key = "cats"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    password = Column(String(12))
    
    def __repr__(self):
        return "<User(name='%s', password='%s')>" % (self.name, self.password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['username'] == '' or request.form['password'] == '':
            error ='wrong login or password'
        else:
            user = User(name=request.form['username'], password=request.form['password'])
            db_session.add(user)
            db_session.commit()
            flash('Registered')
    return render_template('register.html', error=error)

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
def log():
    error = None
    if request.method == 'POST':
        entity = False
        for user in db_session.query(User).filter(User.name == request.form['username'], User.password == request.form['password']):
            entity = True
        if entity == False:
            error ='wrong login or password'
        else:
            session['logged_in'] = True
            return redirect(url_for('wykop'))
    return render_template('log.html', error=error)

@app.route('/wykop')
@login_required
def wykop():
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
