import sys

from os import path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton,
                             QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap
from utils import data_json


class VentanaEspera(QWidget):
    #                               (users)
    senal_iniciar_juego = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.ancho_ventana = data_json("ANCHO_VENTANA")
        self.alto_ventana = data_json("ALTO_VENTANA")

        self.setGeometry(data_json("POS_VENTANA")[0], data_json("POS_VENTANA")[1],
                         self.ancho_ventana, self.alto_ventana)

        self.setWindowTitle("DCCasillas")

        self.ruta_spites = path.join(*data_json("RUTA_SPRITES"))

        self.frames_usuarios = []

        # Diccionario pixmaps iconos
        self.iconos = {
            "rojo": QPixmap(
                path.join(self.ruta_spites, "Fichas", "Simples", "ficha-roja.png")),
            "amarillo": QPixmap(
                path.join(self.ruta_spites, "Fichas", "Simples", "ficha-amarilla.png")),
            "azul": QPixmap(
                path.join(self.ruta_spites, "Fichas", "Simples", "ficha-azul.png")),
            "verde": QPixmap(
                path.join(self.ruta_spites, "Fichas", "Simples", "ficha-verde.png"))
        }

    def cargar_pantalla(self, admin: bool, usuarios: list = []):
        self.admin = admin

        # Imagen fondo
        self.fondo = QLabel(self)
        pixmap_fondo = QPixmap(path.join(self.ruta_spites, "Logos", "fondo.png"))
        self.fondo.setPixmap(pixmap_fondo)
        self.fondo.setGeometry(0, 0, self.ancho_ventana, self.alto_ventana)
        self.fondo.setScaledContents(True)

        # Label titular
        self.titular = QLabel("Esperando a iniciar la partida", self)
        self.titular.setObjectName("titulo")

        # Boton iniciar partida
        self.boton_jugar = QPushButton("Iniciar Partida", self)
        self.boton_jugar.clicked.connect(self.iniciar_juego)
        self.boton_jugar.setEnabled(False)  # Boton desabilitado por default

        # HL titular
        hl1 = QHBoxLayout()
        hl1.addStretch(1)
        hl1.addWidget(self.titular)
        hl1.addStretch(1)

        # VL usuarios
        self.vl1 = QVBoxLayout()
        self.cargar_usuarios(usuarios)

        # HL usuarios
        hl2 = QHBoxLayout()
        hl2.addStretch(1)
        hl2.addLayout(self.vl1)
        hl2.addStretch(1)

        # HL boton
        hl3 = QHBoxLayout()
        hl3.addStretch(1)
        hl3.addWidget(self.boton_jugar)
        hl3.addStretch(1)

        # VL global
        self.vl2 = QVBoxLayout()
        self.vl2.addStretch(1)
        self.vl2.addLayout(hl1)
        self.vl2.addStretch(1)
        self.vl2.addLayout(hl2)
        self.vl2.addStretch(1)
        self.vl2.addLayout(hl3)
        self.vl2.addStretch(1)

        self.setLayout(self.vl2)

        self.mostrar()

    def cargar_usuarios(self, usuarios: list) -> int:
        # Quitar todas las tarjetas actuales
        # numero = self.vl1.count()

        for frame in self.frames_usuarios:
            frame.hide()
            frame.setParent(None)

        for user in usuarios:
            label_nombre = QLabel(user["usuario"], self)
            label_color = QLabel(user["color"], self)
            label_icono = QLabel(self)
            label_icono.setPixmap(self.iconos[user["color"]])

            # HL tarjeta usuario
            hl = QHBoxLayout()
            hl.addStretch(1)
            hl.addWidget(label_nombre)
            hl.addStretch(2)
            hl.addWidget(label_color)
            hl.addStretch(2)
            hl.addWidget(label_icono)

            frame = QFrame(self)
            frame.setObjectName("tarjeta-sala-espera")
            frame.setFixedWidth(self.ancho_ventana * 0.5)
            frame.setLayout(hl)
            self.vl1.addWidget(frame)
            self.frames_usuarios.append(frame)

        if self.admin and len(usuarios) >= data_json("MINIMO_JUGADORES"):
            self.boton_jugar.setEnabled(True)

        self.usuarios = usuarios
        self.repaint()

    def iniciar_juego(self):
        mensaje = {
            "comando": "iniciar_partida",
            "usuarios": self.usuarios
        }
        self.senal_iniciar_juego.emit(mensaje)

    def mostrar(self):
        self.show()

    def esconder(self):
        self.hide()
