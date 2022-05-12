from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QHBoxLayout, QLayout, QWidget


def encapsular_h(object: QObject) -> QHBoxLayout:
    hbox = QHBoxLayout()
    hbox.addStretch(1)
    if isinstance(object, QWidget):
        hbox.addWidget(object)
    elif isinstance(object, QLayout):
        hbox.addLayout(object)
    hbox.addStretch(1)

    return hbox
