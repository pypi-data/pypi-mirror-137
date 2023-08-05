from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from ..bases import To7mQtWidget


class FileDialog(To7mQtWidget, QFileDialog):
    @classmethod
    def getExistingDirectory(cls, *xargs, **kwargs):
        return Path(super().getExistingDirectory(*xargs, **kwargs))

    def setDirectory(self, path):
        return super().setDirectory(str(path))
