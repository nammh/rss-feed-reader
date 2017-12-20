# Copyright 2017 Moohyeon Nam
# Modified 2017-12-18

import os
import sqlite3
import opml_handler
import rss_handler
import feedfilter as flt

def add_source(item):
    con = sqlite3.connect("feed.db")
    cur = con.cursor()
    try:
        cur.execute("insert into feed (title, url, type) values (?, ?, ?)", 
                (item["title"], item["url"], item["type"]))
    except sqlite3.IntegrityError:
        print("The feed (?, ?, ?) is already exists in the database.",
                (item["title"], item["url"], item["type"]))
    con.commit()
    con.close()

def show_sources():
    con = sqlite3.connect("feed.db")
    cur = con.cursor()
    for feed in cur.execute("select * from feed;"):
        print(feed)
    con.close()

def get_update():
    con = sqlite3.connect("feed.db")
    cur = con.cursor()
    cur.execute("select url from feed;")
    feeds = cur.fetchall()
    for feed in feeds:
        for item in rss_handler.getArticle(feed[0]):
            title, url, description, date, source = item
            try:
                cur.execute("insert into articles values (?, ?, ?, ?, ?)",
                        (url, title, description, date, source))
            except sqlite3.IntegrityError:
                print("get_update(): sqlite3.IntegrityError")
                print(item)
                continue
    con.commit()
    con.close()

def get_feed():
    feed = []
    con = sqlite3.connect("feed.db")
    cur = con.cursor()
    for item in cur.execute("select date, title, url, source from articles order by date desc, title, url;"):
        feed.append({"date":item[0],
                     "title":item[1],
                     "url":item[2],
                     "source":item[3]})
    con.close()
    return feed

if __name__=='__main__':
    _filter = flt.get_filter('filter.txt')
    get_update()
    with open('test.html', 'w', encoding='utf-8') as ofs:
        for item in get_feed():
            if flt.filtering(item["title"], _filter):
                ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                    item["date"], item["url"], item["title"], item["source"]))

'''
# Table schema
      cur.execute("create table feed(title text, url text primary key, type text);")
      cur.execute("create table articles(url text primary key, title text, description text, date timestamp, source text);")
'''
