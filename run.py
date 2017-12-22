import time
import datetime
import db_handler as db
import feedfilter as flt

_filter = flt.get_filter('filter.txt')  # Should be replaced with db
try:
    while True:
        db.get_update()
        with open('output.html', 'w', encoding='utf-8') as ofs:
            for item in db.get_feed():
                if flt.filtering(item["title"], _filter):
                    ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                        item["date"], item["url"], item["title"], item["source"]))
        print("[Updated] " + str(datetime.datetime.now()))
        time.sleep(3600)
        # want to add a key to refresh without this delay... HOW?
except KeyboardInterrupt:
    print("Exit.")
    with open('output.html', 'w', encoding='utf-8') as ofs:
        for item in db.get_feed():
            if flt.filtering(item["title"], _filter):
                ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                    item["date"], item["url"], item["title"], item["source"]))
