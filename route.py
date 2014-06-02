from flask import *
import feedparser
import re

app = Flask(__name__)

# klasa musi dziedziczyc po obiekcie object brakuje tez docstringa do czego
# sluzy
class data():
    def __init__(self, title, img):
        self.title = title
        self.img = img

# funkcji brakuje docstringa
@app.route('/test')
def test(): #funkcja zwraca dane ze strony do test.html, niestety nie dziala
    feed = feedparser.parse('http://www.wykop.pl/rss/')
    title = []
    img = []
    # Jak sie iteruje po tablicy? Z pewnoscia nie tak, ranga wogole sie nie 
    # uzywa, bo generuje cala liste od razu. Uzywaj xrange. Poprawnie powinno
    # byc: for i in feed['entries']
    for i in range(0,10):
        # miast feed['entries'][i]['title'] apendujesz samo i['title']
        title.append(feed['entries'][i]['title'])
        # tutaj podobnie
        img.append(re.findall('<img src="(.*?)" />', feed['entries'][i]['description']))
    # Do tego typu rzeczy uzywamy sowniki, nie tworzymy klasy. wiesz, ze do
    # self.title i self.img wkladasz dwie tablice, ktore nie maja ze soba logi-
    # cznego powiazania? Slownie JEDNA INSTANCJA klasy. Jak juz piszesz w ten
    # sposob (nie polecam w przyszlosci robic takich rzeczy, jezeli nie jest to
    # faktycznie konieczne, to badz konsekwentny, napisz setery i getery, doc-
    # stringi do wszystkiego, uzywaj tego w logiczny sposob, i zanim wysles cos
    # do recenzji, nie stweirdzaj nie dziala i nie wiem dla czego, bo jezeli 
    # piszesz w c++ to powinienes wiedziec jak sie robi takie rzeczy)
    info = data(title,img)
    # zagladajac do templejtki widze, ze probujesz sie iterowac po data. W jaki
    # sposob? Stworzyles obiekt w ktorym trzymasz dwie tablice. iterujesz sie
    # po nich osobno, albo ogarniasz to w jakis bardziej sensowny sposob. Nie
    # zdefiniowales metody next, wiec python nie wie jak sie po czyms takim 
    # iterowac.
    return render_template('test.html', data=info)

@app.route('/')
def home():
    return render_template('home.html')

# wszystko jak powyzej. Mowilem Ci o pdb, z nim problem rozwiazalbys w chwile
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

# ta metode ciezko jest skomentowac, ale rozumiem, ze jestes niedoswiadczony
# i nie dogadalismy sie dobrze. Prosta metoda logowania, tak powiedzialem, ale
# chodzilo mi o jakies gotowe logiczne rozwiazanie, to NIE JEST system
# logowania. Bazy danych/hashowanie hasel/cokolwiek zwiazanego z seciurity
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
