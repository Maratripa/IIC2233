from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap

from utils import data_json


class VentanaFinal(QWidget):

    senal_volver_inicio = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.ancho_ventana = data_json("ANCHO_VENTANA")
        alto_ventana = data_json("ALTO_VENTANA")
        pos_ventana = data_json("POS_VENTANA")

        self.setGeometry(pos_ventana[0], pos_ventana[1],
                         self.ancho_ventana,  alto_ventana)
        self.setWindowTitle("DCCasillas")

        # Imagen fondo
        self.fondo = QLabel(self)
        pixmap_fondo = QPixmap(path.join(*data_json("RUTA_SPRITES"), "Logos", "fondo.png"))
        self.fondo.setPixmap(pixmap_fondo)
        self.fondo.setGeometry(0, 0, self.ancho_ventana, alto_ventana)
        self.fondo.setScaledContents(True)

        self.frames = []

        self.label_ganador = QLabel(f"¡Felicidades {''}!", self)
        self.label_ganador.setObjectName("titulo")

        boton_volver = QPushButton("Volver al inicio", self)
        boton_volver.clicked.connect(self.volver_inicio)

        # HL ganador
        hl1 = QHBoxLayout()
        hl1.addStretch(1)
        hl1.addWidget(self.label_ganador)
        hl1.addStretch(1)

        # VL jugadores
        self.vl1_1 = QVBoxLayout()

        # VL global
        vl1 = QVBoxLayout()
        vl1.addStretch(1)
        vl1.addLayout(hl1)
        vl1.addStretch(1)
        vl1.addLayout(self.vl1_1)
        vl1.addStretch(1)
        vl1.addWidget(boton_volver)
        vl1.addStretch(1)

        # HL global
        hl2 = QHBoxLayout()
        hl2.addStretch(1)
        hl2.addLayout(vl1)
        hl2.addStretch(1)

        self.setLayout(hl2)

    def cargar_usuarios(self, ganador: str, usuarios: list):
        self.label_ganador.setText(f"¡Felicidades {ganador}!")

        for f in self.frames:
            f.hide()
            f.setParent(None)

        for user in usuarios:
            label_nombre = QLabel(f"{user['usuario']}", self)
            label_en_base = QLabel(f"Fichas en base:  {user['en_base']}", self)
            label_en_color = QLabel(f"Fichas en color: {user['en_color']}", self)
            label_en_victoria = QLabel(f"Fichas victoria: {user['en_victoria']}", self)

            # VL nombre
            vl1 = QVBoxLayout()
            vl1.addStretch(1)
            vl1.addWidget(label_nombre)
            vl1.addStretch(1)

            # VL datos
            vl2 = QVBoxLayout()
            vl2.addWidget(label_en_base)
            vl2.addWidget(label_en_color)
            vl2.addWidget(label_en_victoria)

            # HL tarjeta
            hl = QHBoxLayout()
            hl.setSpacing(10)
            hl.addStretch(1)
            hl.addLayout(vl1)
            hl.addStretch(3)
            hl.addLayout(vl2)
            hl.addStretch(1)

            frame = QFrame(self)
            frame.setObjectName("tarjeta-usuario-juego")
            frame.setFixedWidth(self.ancho_ventana * 0.5)
            frame.setLayout(hl)
            self.frames.append(frame)

            self.vl1_1.addWidget(frame)
        
        self.repaint()
        self.mostrar()
    
    def volver_inicio(self):
        self.senal_volver_inicio.emit()

    def mostrar(self):
        self.show()
    
    def esconder(self):
        self.hide()
