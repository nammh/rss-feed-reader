# Copyright 2017 Moohyeon Nam
# Modified 2017-12-28

import sys
import os
import sqlite3
import datetime
import opml_handler
import rss_handler
import datetime_util
import feedfilter as flt

def exec_n_fetch(cur, stmt):
    cur.execute(stmt)
    return cur.fetchall()

def update_source(cur, src):
    res = exec_n_fetch(cur, "select url, id from feed where url='{}'".format(src))
    for item in rss_handler.getArticle(res[0][0], res[0][1]):
        title, url, desc, date, src = item
        try:
            cur.execute ("insert into article (title, url, desc, date, src) values (?, ?, ?, ?, ?)", (url, title, desc, date, src))
        except sqlite3.IntegrityError:
            print("update_source(): sqlite3.IntegrityError")
            print(item)
            continue

def get_update(cur):
    last = datetime_util.parse(exec_n_fetch
            (cur, "select max(time) from time_table where type=0")[0][0])
    for feed in exec_n_fetch(cur, "select url, id from feed"):
        for item in rss_handler.getArticle(feed[0], feed[1]):
            title, url, desc, date, src = item
            try:
                if date > last:
                    cur.execute("insert into article values (null, ?, ?, ?, ?, ?)", (title, url, desc, date, src))
            except sqlite3.IntegrityError:
                print("get_update(): sqlite3.IntegrityError")
                print(item)
                continue
    cur.execute("insert into time_table (time, type) values (?, 0)",
            (datetime.datetime.now(),))

def get_feed(cur):
    ret = []
    for item in exec_n_fetch(cur, "select t1.title, t1.url, t1.desc, t1.date, t2.title from article t1 inner join feed t2 where t1.src = t2.id order by t1.date desc"):
        ret.append({"title":item[0], "url":item[1], "desc":item[2],
            "date":item[3], "source":item[4]})
    return ret

if __name__=='__main__':
    print("db_handler.py")
