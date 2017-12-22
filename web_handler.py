# Copyright 2017 Moohyeon Nam
# Modified 2017-12-18

import requests
from bs4 import BeautifulSoup

def get(url):
    try:
        req = requests.get(url)
        return req.text
    except requests.exceptions.ConnectionError:
        print(url)
        return ""

def findrss(url):
    soup = BeautifulSoup(get(url), "html.parser")
    for elem in soup.find_all("a", href=True):
        if 'rss' in elem["href"]:
            return(elem["href"])
    for elem in soup.find_all("link", href=True):
        if 'rss' in elem["href"]:
            return(elem["href"])

if __name__ == "__main__":
    print(get(findrss("http://babnsool.egloos.com/")))
