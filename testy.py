import feedparser
import re

feed = feedparser.parse('http://www.wykop.pl/rss/')

title = []
desc = []
url = []
img = []
napis = "<title>sdf</title>"

class data():
    def __init__(self, title, img):
        self.title = title
        self.img = img

for i in range(0,10):
    title.append(feed['entries'][i]['title'])
    desc.append(feed['entries'][i]['description'])
    url.append(feed['entries'][i]['link'])
    img.append(re.findall('<img src="(.*?)" />', feed['entries'][8]['description']))

info = data(title, img)

info2 = info

#for j in range(0,10):
#    print "-------------------------------------\n"
#    print "Post %s: " % (j+1)
#    print "\n"
#    print "Tytul: ", title[j]
#    print "\n"
#    print "Opis: ", desc[j]
#    print "\n"
#    print "URL: ", url[j]
#    print "\n"
#    print "IMG: ", img[j][0]
#    print "-------------------------------------\n"
for item in range(0,10):
    print info2.title[item]
    print info2.img[item][0]

