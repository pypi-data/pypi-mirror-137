from PySide6.QtWidgets import QButtonGroup

from ..bases import To7mQtWidget


class ButtonGroup(To7mQtWidget, QButtonGroup):
    def __init__(self, *xargs, **kwargs):
        super().__init__(*xargs, **kwargs)

        super().setExclusive(False)
        self._exclusive = False
        self._allowUntick = True
        self.buttonClicked.connect(self._onClick)

    def _onClick(self, clicked_button):
        if clicked_button.isChecked():
            if self._exclusive:
                for button in self.buttons():
                    if button is not clicked_button:
                        button.setChecked(False)
        else:
            if not self.allow_untick:
                clicked_button.setChecked(True)

    def setExclusive(self, mode=True):
        self._exclusive = mode

    def setAllowUntick(self, mode=True):
        self._allowUntick = mode
