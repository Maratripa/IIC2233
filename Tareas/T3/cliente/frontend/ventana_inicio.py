import sys

from os import path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton,
                             QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from utils import data_json


class VentanaInicio(QWidget):

    senal_enviar_usuario = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.setGeometry(data_json("POS_VENTANA")[0], data_json("POS_VENTANA")[1],
                         data_json("ANCHO_VENTANA"),  data_json("ALTO_VENTANA"))

        self.setWindowTitle("Bienvenido a DCCasillas!")

        # Imagen fondo
        self.fondo = QLabel(self)
        pixmap_fondo = QPixmap(path.join(*data_json("RUTA_SPRITES"), "Logos", "fondo.png"))
        self.fondo.setPixmap(pixmap_fondo)
        self.fondo.setGeometry(0, 0, data_json("ANCHO_VENTANA"), data_json("ALTO_VENTANA"))
        self.fondo.setScaledContents(True)

        # Imagen logo
        self.logo = QLabel(self)
        pixmap_logo = QPixmap(path.join(*data_json("RUTA_SPRITES"), "Logos", "logo.png"))
        self.logo.setPixmap(pixmap_logo)
        self.logo.setScaledContents(True)

        # Input field
        self.input_usuario = QLineEdit(self)
        self.input_usuario.setPlaceholderText("Ingresa tu usuario")

        # Boton
        self.boton_validar = QPushButton("JUGAR", self)
        self.boton_validar.clicked.connect(self.enviar_usuario)

        # HL logo
        hl1 = QHBoxLayout()
        hl1.addStretch(1)
        hl1.addWidget(self.logo)
        hl1.addStretch(1)

        # HL input
        hl2 = QHBoxLayout()
        hl2.addStretch(1)
        hl2.addWidget(self.input_usuario)
        hl2.addStretch(1)

        # HL boton
        hl3 = QHBoxLayout()
        hl3.addStretch(1)
        hl3.addWidget(self.boton_validar)
        hl3.addStretch(1)

        # VL global
        vl1 = QVBoxLayout()
        vl1.addStretch(1)
        vl1.addLayout(hl1)
        vl1.addStretch(1)
        vl1.addLayout(hl2)
        vl1.addLayout(hl3)
        vl1.addStretch(1)

        self.setLayout(vl1)

    def mostrar(self):
        self.show()

    def esconder(self):
        self.hide()

    def enviar_usuario(self):
        self.senal_enviar_usuario.emit({
            "comando": "validar_login",
            "usuario": self.input_usuario.text()
        })

    def error_usuario(self, error: str):
        self.input_usuario.setText("")
        self.input_usuario.setPlaceholderText(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaInicio()
    ventana.mostrar()
    sys.exit(app.exec_())
