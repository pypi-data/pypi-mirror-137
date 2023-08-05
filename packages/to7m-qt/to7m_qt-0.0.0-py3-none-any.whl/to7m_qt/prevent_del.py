_prevent_del = set()


def add(obj):
    _prevent_del.add(obj)


def clear():
    _prevent_del = set()
