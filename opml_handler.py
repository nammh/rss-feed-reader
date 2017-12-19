import sys
from bs4 import BeautifulSoup

def parse(path):
    content = ''
    with open(path, 'r', encoding='utf-8') as ifs:
        for line in ifs:
            content+=line
    soup = BeautifulSoup(content, 'xml')
    contentList = []
    for item in soup.find_all('outline'):
        if item.get("type", "") != "":
            contentList.append(
                    {"title":item.get("title",""), 
                    "url": item.get("xmlUrl",""),
                    "type": item.get("type","")
                    })
    return contentList

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python " + sys.argv[0] + " target.opml");
        sys.exit()

    contentList = parse(sys.argv[1])
    contentList.sort(key=lambda x: x['title'])
    for item in contentList:
        print(item['type'], item['title'], item['url'])
