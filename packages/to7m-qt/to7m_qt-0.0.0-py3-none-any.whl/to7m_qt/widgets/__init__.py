from PySide6 import QtWidgets

from ..bases import To7mQtWidget
from .core_application import Application
from .button_group import ButtonGroup
from .file_dialog import FileDialog


top_level = {"Application": Application,
             "ButtonGroup": ButtonGroup,
             "FileDialog": FileDialog}


for name, obj in QtWidgets.__dict__.items():
    if not name.startswith('Q'):
        continue

    name = name[1:]
    if name in globals():
        continue

    mcls = type(obj)
    bases = To7mQtWidget, obj
    attrs_dict = {"__module__": __name__, "__qualname__": name}
    try:
        cls = mcls(name, bases, attrs_dict)
        globals()[name] = cls
        top_level[name] = cls
    except TypeError as err:
        pass
