import feedparser
from bs4 import BeautifulSoup
from flask import *


app = Flask(__name__)


@app.route('/')
def index():
    """
    Render view with ten news from wykop.
    """
    feed = feedparser.parse('http://www.wykop.pl/rss/')
    data = []
    for entry in feed['entries'][:10]:
        # Very usefull library! I don't use it, becouse i don't need.
        # Python has a lot of usefull library.
        img = BeautifulSoup(entry['summary']).img
        data.append({
                'link' : entry['link'],
                'title': entry['title'],
                'summary': entry['summary'],
                'published': entry['published']
                })
    return render_template('feed.html', data=data)


if __name__ == '__main__':
    app.run()
