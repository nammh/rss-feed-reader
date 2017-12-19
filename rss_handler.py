# Copyright 2017 Moohyeon Nam
# Modified 2017-12-18

import web_handler as wh
from bs4 import BeautifulSoup
import datetime
import operator

import datetime_util
import opml_handler

def getArticle(url):
    soup = BeautifulSoup(wh.get(url), "xml")
    articles = []
    for item in soup.find_all("item"):
        try:
            articles.append((item.title.text.encode('utf-8').decode(),
                            item.link.text,
                            item.description.text,
                            datetime_util.parse(item.pubDate.text),
                            soup.channel.title.text
                            ))
        except AttributeError:
            print("AttributeError: " + soup.channel.title.text)
            return []
        except ValueError:
            print("ValueError: " + soup.channel.title.text)
            return []
    return articles

if __name__=="__main__":
    info = []

    cl = opml_handler.parse("./feedly_feed.opml")
    for item in cl:
        info += getArticle(item["url"])
    #  url = "http://bbs.ruliweb.com/news/537/rss"
    #  info += getArticle(url)
    #  url = "http://blog.naver.com/a1231724/"
    #  info += getArticle(wh.findrss(url))
    #  url = "http://babnsool.egloos.com/"
    #  info += getArticle(wh.findrss(url))
    #  url = 'https://www.sangkon.com/'
    #  info += getArticle(wh.findrss(url))
    #  for item in info:
    #      print(item[3], item[0], item[1])
    info.sort(reverse=True, key=operator.itemgetter(3))

    ofs = open("test.html", "w", encoding='utf-8')
    ofs.write("<html><body>")
    for art in info:
        ofs.write("<p>")
        ofs.write("{} <a href='{}'>{}</a> - {}".format(str(art[3]), art[1], art[0], art[4]))
        ofs.write("</p>")
    ofs.write("</body></html>")
    ofs.close()
