from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QHBoxLayout


def encapsular_h(widget: QObject) -> QHBoxLayout:
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    hbox.addWidget(widget)
    hbox.addStretch(1)

    return hbox
