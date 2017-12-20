def filtering(_target, _filter):
    for f in _filter:
        if f in _target:
            return False
    return True

def get_filter(path):
    filterlist = []
    with open(path, 'r', encoding='utf-8') as ifs:
        for line in ifs:
            filterlist.append(line.strip())
    return filterlist
