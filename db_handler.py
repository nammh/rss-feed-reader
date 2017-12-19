# Copyright 2017 Moohyeon Nam
# Modified 2017-12-18

import sqlite3
import opml_handler
import rss_handler

if __name__=='__main__':
    #  info = []
    cl = opml_handler.parse("./feedly_feed.opml")
    #  for item in cl:
    #      info += getArticle(item["url"])
    #  info.sort(reverse=True, key=operator.itemgetter(3))
    con = sqlite3.connect("feed.db")
    cur = con.cursor()
    #  cur.execute("drop table feed;")
    #  cur.execute("drop table articles;")
    #  cur.execute("create table feed(title text, url text primary key, type text);")
    #  cur.execute("create table articles(url text primary key, title text, description text, date timestamp, source text);")
    #  for item in cl:
    #      cur.execute("insert into feed (title, url, type) values (\"{}\",\"{}\",\"{}\");".format(item["title"], item["url"], item["type"]))
    cur.execute("select * from feed;")
    feeds = cur.fetchall()
    for feed in feeds:
        for article in rss_handler.getArticle(feed[1]):
            a,b,c,d,e = article
            try:
                cur.execute("insert into articles values (?, ?, ?, ?, ?)",
                        (b,a,c,d,e))
            except sqlite3.IntegrityError:
                continue

    with open('test.html', 'w', encoding='utf-8') as ofs:
        for item in cur.execute("select date, title, url, source from articles order by date desc, title, url;"):
            ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                item[0], item[2], item[1], item[3]))
    con.commit()
    con.close()
