from PySide6.QtWidgets import QApplication

from .. import prevent_del
from ..bases import To7mQtWidget


class Application(To7mQtWidget, QApplication):
    def exec(self):
        try:
            return super().exec()
        finally:
            prevent_del.clear()
