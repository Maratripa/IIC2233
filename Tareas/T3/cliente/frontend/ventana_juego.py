from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout)
from PyQt5.QtGui import QPixmap

from utils import data_json


class VentanaJuego(QWidget):
    def __init__(self):
        super().__init__()

        ancho_ventana = data_json("ANCHO_VENTANA")
        alto_ventana = data_json("ALTO_VENTANA")
        pos_ventana = data_json("POS_VENTANA")

        self.setGeometry(pos_ventana[0], pos_ventana[1],
                         ancho_ventana,  alto_ventana)
        self.setWindowTitle("DCCasillas")

        self.pixmaps = {
            "tablero": QPixmap("Sprites/Juego/tablero.png"),  # TODO
            "dado": QPixmap("Spreites/Logos/dado.png"),  # TODO
            "estrella": QPixmap("Sprites/Juego/estrella.png"),
            "logo": QPixmap("Sprites/Logos/logo.png")
        }

    def init_gui(self):
        self.tablero = QLabel(self)
        self.tablero.setPixmap(self.pixmaps["tablero"])

        self.dado = QLabel(self)
        self.dado.setPixmap(self.pixmaps["dado"])
