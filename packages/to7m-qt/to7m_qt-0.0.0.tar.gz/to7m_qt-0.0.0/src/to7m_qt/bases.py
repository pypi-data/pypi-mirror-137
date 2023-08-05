from . import prevent_del


class To7mQt:
    pass


class To7mQtWidget(To7mQt):
    def __init__(self, *xargs, **kwargs):
        super().__init__(*xargs, **kwargs)
        prevent_del.add(self)
