import db_handler as db
import feedfilter as flt

_filter = flt.get_filter('filter.txt')  # Should be replaced with db
db.get_update()
with open('output.html', 'w', encoding='utf-8') as ofs:
    for item in db.get_feed():
        if flt.filtering(item["title"], _filter):
            ofs.write("<p>{} - <a href={}>{}</a> - {}</p>".format(
                item["date"], item["url"], item["title"], item["source"]))
