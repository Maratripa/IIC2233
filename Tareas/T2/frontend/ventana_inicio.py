import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton)
# import parametros as p #TODO


class VentanaInicio(QWidget):

    senal_jugar = pyqtSignal()
    senal_ranking = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Geometria
        self.setGeometry(600, 200, 600, 600)
        self.setWindowTitle("A cazar aliens!")
        self.setStyleSheet("background-color: #1A1826;")
        self.crear_elementos()

    def crear_elementos(self):
        self.logo = QLabel(self)
        pixmap = QPixmap(
            "assets/Sprites/Logo/Logo.png").scaled(400, 300, 1, 1)  # TODO
        self.logo.setPixmap(pixmap)

        self.boton_jugar = QPushButton("Jugar", self)
        self.boton_jugar.setStyleSheet("background-color: #575268;")
        self.boton_jugar.clicked.connect(self.jugar)

        self.boton_ranking = QPushButton("Ranking", self)
        self.boton_ranking.setStyleSheet("background-color: #575268;")
        self.boton_ranking.clicked.connect(self.ranking)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.boton_jugar)
        vbox1.addWidget(self.boton_ranking)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addLayout(vbox1)
        hbox1.addStretch(1)

        vbox2 = QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.logo)
        vbox2.addStretch(1)
        vbox2.addLayout(hbox1)
        vbox2.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox2)
        hbox2.addStretch(1)

        self.setLayout(hbox2)

    def jugar(self):
        self.senal_jugar.emit()
        self.esconder()

    def ranking(self):
        self.senal_ranking.emit()
        self.esconder()

    def mostrar(self):
        self.show()

    def esconder(self):
        self.hide()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.mostrar()
    sys.exit(app.exec_())
