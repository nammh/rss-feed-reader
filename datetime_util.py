import datetime
import re

def extract(timestr):
    if re.search(r"\d+.\d+.\d+ \(\d+:\d+:\d+\)", timestr):
        return timestr, "%Y.%m.%d (%H:%M:%S)"
    elif re.search(r"\w+, \d+ \w+ \d+ \d+:\d+:\d+ \+\d+", timestr):
        return timestr, "%a, %d %b %Y %H:%M:%S %z"
    elif re.search(r"\w+, \d+ \w+ \d+ \d+:\d+:\d+ \w+", timestr):
        return timestr, "%a, %d %b %Y %H:%M:%S %Z"
    elif re.search(r"\d+-\d+-\d+ \d+:\d+:\d+.\d+\+\d+:\d+", timestr):
        pos = timestr.find('+')
        timestr = timestr[:pos]
        return timestr, "%Y-%m-%d %H:%M:%S.%f"
    elif re.search(r"\d+-\d+-\d+ \d+:\d+:\d+.\d+", timestr):
        return timestr, "%Y-%m-%d %H:%M:%S.%f"
    elif re.search(r"\d+:\d+", timestr):
        now = datetime.datetime.now().astimezone()
        return extract(now.strftime("%a, %d %b %Y " + timestr + ":%S %z"))
    elif re.search(r"\d+.\d+.\d+", timestr):
        return extract(timestr + " (00:00:00)")
    else:
        print(timestr)
        return timestr, "FAILED"

def parse(timestr):
    original, parsed = extract(timestr)
    return datetime.datetime.strptime(original, parsed).astimezone()

if __name__ == "__main__":
    test_set = []
    test_set.append("2017.12.18 (17:28:56)")
    test_set.append("Mon, 18 Dec 2017 18:00:00 +0900")
    test_set.append("Mon, 18 Dec 2017 18:00:00 GMT")
    test_set.append("00:39")
    test_set.append("2017.12.18")
    test_set.append("2017-12-22 15:37:14.781591")

    for item in test_set:
        print(item)
        print(parse(item))
