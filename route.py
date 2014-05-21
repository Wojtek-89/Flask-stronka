from flask import *
import feedparser
import re

app = Flask(__name__)

class data():
    def __init__(self, title, img):
        self.title = title
        self.img = img

@app.route('/test')
def test(): #funkcja zwraca dane ze strony do test.html, niestety nie dziala
    feed = feedparser.parse('http://www.wykop.pl/rss/')
    title = []
    img = []
    for i in range(0,10):
        title.append(feed['entries'][i]['title'])
        img.append(re.findall('<img src="(.*?)" />', feed['entries'][i]['description']))
    info = data(title,img)
    return render_template('test.html', data=info)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/hello')
def hello():
    feed = feedparser.parse('http://www.wykop.pl/rss/')
    title = []
    img = []
    for i in range(0,4):
        title.append(feed['entries'][i]['title'])
        img.append(re.findall('<img src="(.*?)" />', feed['entries'][i]['description']))
    return render_template('hello.html', title1=title[0],
                                         title2=title[1],
                                         title3=title[2],
                                         title4=title[3],
                                         img1=img[0][0],
                                         img2=img[1][0],
                                         img3=img[2][0],
                                         img4=img[3][0])

@app.route('/log', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username']!='admin' or request.form['password']!='password':
            error="Inwalid username or password!"
        else:
            return redirect(url_for('hello'))
    return render_template('log.html',error=error)

if __name__ == '__main__':
    app.run()
