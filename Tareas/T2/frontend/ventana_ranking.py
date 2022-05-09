import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QScrollArea,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QFormLayout, QFrame)

from manejo_archivos import cargar_puntajes


class VentanaRanking(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Geometria
        self.setGeometry(600, 200, 600, 600)
        self.setWindowTitle("A cazar aliens!")
        self.setStyleSheet("background-color: #1A1826;")
        self.crear_elementos()

    def crear_elementos(self):

        self.ranking = QFormLayout(self)
        self.cargar_ranking()

        self.frame = QFrame(self)
        self.frame.setLayout(self.ranking)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidget(self.frame)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(300)

        self.titulo = QLabel("Ranking", self)
        self.titulo.setStyleSheet("color: white;")

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.titulo)
        hbox1.addStretch(1)

        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.setStyleSheet("background-color: #575268;")

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.boton_volver)
        hbox2.addStretch(1)

        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addLayout(hbox1)
        vbox1.addStretch(1)
        vbox1.addWidget(self.scroll_area)
        vbox1.addStretch(1)
        vbox1.addLayout(hbox2)
        vbox1.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addLayout(vbox1)
        hbox3.addStretch(1)

        self.setLayout(hbox3)
        self.show()

    def cargar_ranking(self):
        puntajes = cargar_puntajes()

        for linea in puntajes:
            usuario = QLabel(linea[0], self)
            usuario.setStyleSheet("color: white;")
            score = QLabel(f"{linea[1]} ptos", self)
            score.setStyleSheet("color: white;")

            self.ranking.addRow(usuario, score)


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaRanking()
    sys.exit(app.exec_())
