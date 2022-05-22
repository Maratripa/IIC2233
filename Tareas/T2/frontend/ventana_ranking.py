from os import path
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton,
                             QFormLayout, QFrame)

from manejo_archivos import cargar_puntajes
import utils
import parametros as p


class VentanaRanking(QWidget):

    senal_volver = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO / 2, p.VENTANA_ALTO)
        self.setWindowTitle("A cazar aliens!")

        # Label titulo
        self.titulo = QLabel("Ranking", self)
        self.titulo.setObjectName("titulo")

        # FormLayout con puntajes
        self.ranking = QFormLayout()
        self.ranking.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.ranking.setHorizontalSpacing(50)
        self.ranking.setVerticalSpacing(40)
        self.cargar_ranking()

        # Boton volver al menu de inicio
        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.clicked.connect(self.volver)

        # Vbox de contenidos
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addLayout(utils.encapsular_h(self.titulo))
        vbox1.addStretch(1)
        vbox1.addLayout(self.ranking)
        vbox1.addStretch(1)
        vbox1.addLayout(utils.encapsular_h(self.boton_volver))
        vbox1.addStretch(1)

        # Hbox para centrar objetos
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addLayout(vbox1)
        hbox3.addStretch(1)

        self.setLayout(hbox3)

    def mostrar(self):
        for i in range(self.ranking.rowCount() - 1, -1, -1):
            self.ranking.removeRow(i)

        self.cargar_ranking()
        self.show()

    # Rellenar FormLayout
    def cargar_ranking(self):
        puntajes = cargar_puntajes()  # Lista ordenada de puntajes y usuarios

        # Obtener mejores 5 puntajes
        for i in range(5):
            usuario = QLabel(f"{i + 1}. {puntajes[i][0]:13.13}", self)
            usuario.setObjectName("puntajes")

            score = QLabel(f"{puntajes[i][1]} ptos", self)
            score.setObjectName("puntajes")

            frame = QFrame(self)
            icono = QLabel(frame)
            frame.setFixedSize(80, 50)
            icono.setAlignment(Qt.AlignmentFlag.AlignCenter)

            if i == 0:
                icono.setPixmap(QPixmap(
                    path.join(*p.RUTA_ALIEN, "Alien3.png")).scaled(80, 50, 1, 1))
            elif i == 1:
                icono.setPixmap(QPixmap(
                    path.join(*p.RUTA_ALIEN, "Alien2.png")).scaled(40, 50, 1, 1))
            elif i == 2:
                icono.setPixmap(QPixmap(
                    path.join(*p.RUTA_ALIEN, "Alien1.png")).scaled(46, 50, 1, 1))

            layout = QHBoxLayout()
            layout.addWidget(icono, alignment=Qt.AlignmentFlag.AlignCenter)
            frame.setLayout(layout)
            icono.setScaledContents(True)

            hbox = QHBoxLayout()
            hbox.addWidget(usuario)
            hbox.addStretch(1)
            hbox.addWidget(score)
            hbox.addWidget(frame)

            self.ranking.addRow(hbox)

    # Boton volver
    def volver(self):
        self.hide()
        self.senal_volver.emit()
