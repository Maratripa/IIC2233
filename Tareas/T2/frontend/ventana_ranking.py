import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QScrollArea,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QFormLayout, QFrame)

from manejo_archivos import cargar_puntajes
import parametros as p


class VentanaRanking(QWidget):

    senal_volver = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO, p.VENTANA_ALTO)
        self.setWindowTitle("A cazar aliens!")
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
        self.titulo.setObjectName("titulo")

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.titulo)
        hbox1.addStretch(1)

        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.clicked.connect(self.volver)

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

    def cargar_ranking(self):
        puntajes = cargar_puntajes()

        for linea in puntajes:
            usuario = QLabel(linea[0], self)
            score = QLabel(f"{linea[1]} ptos", self)

            self.ranking.addRow(usuario, score)

    def volver(self):
        self.hide()
        self.senal_volver.emit()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaRanking()
    sys.exit(app.exec_())
