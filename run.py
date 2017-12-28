import sys
import time
import datetime
import sqlite3
import db_handler as db
import feedfilter as flt

_filter = flt.get_filter('filter.txt')  # Should be replaced with db

conn = sqlite3.connect('feed.db')
cur = conn.cursor()

try:
    while True:
        db.get_update(cur)
        with open('output.html', 'w', encoding='utf-8') as ofs:
            for item in db.get_feed(cur):
                if flt.filtering(item["title"], _filter):
                    ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                        item["date"], item["url"], item["title"], item["source"]))
        print("[Updated] " + str(datetime.datetime.now()))
        time.sleep(1800)
        # want to add a key to refresh without this delay... HOW?
except KeyboardInterrupt:
    print("Exit.")
    with open('output.html', 'w', encoding='utf-8') as ofs:
        for item in db.get_feed(cur):
            if flt.filtering(item["title"], _filter):
                ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                    item["date"], item["url"], item["title"], item["source"]))
#  except BaseException:
#      print(*sys.exc_info())

conn.commit()
conn.close()
