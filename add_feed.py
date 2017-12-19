import sys
from bs4 import BeautifulSoup
import web_handler
import db_handler
import opml_handler

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("Usage: python " + sys.argv[0] + " [feedlist]")
        sys.exit()

    feedlist = []
    if sys.argv[1].find(".opml"):
        feedlist += opml_handler.parse(sys.argv[1])
        for item in feedlist:
            db_handler.add_source(item)
    else:
        with open(sys.argv[1], 'r', encoding='utf-8') as ifs:
            for line in ifs:
                feedlist.append({"title":"", "url":line, "type":"rss"});

        for item in feedlist:
            soup = BeautifulSoup(web_handler.get(item["url"]), "xml")
            item["title"] = soup.channel.title.text
            db_handler.add_source(item)
