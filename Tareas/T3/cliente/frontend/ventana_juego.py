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
            "tablero":  QPixmap("Sprites/Juego/tablero.png"),  # TODO
            "dado":     QPixmap("Spreites/Logos/dado.png"),  # TODO
            "estrella": QPixmap("Sprites/Juego/estrella.png"),
            "logo":     QPixmap("Sprites/Logos/logo.png")
        }

        self.fichas = {
            "rojo":             QPixmap("Sprites/Fichas/Simples/ficha-roja.png"),
            "amarillo":         QPixmap("Sprites/Fichas/Simples/ficha-amarilla.png"),
            "verde":            QPixmap("Sprites/Fichas/Simples/ficha-verde.png"),
            "azul":             QPixmap("Sprites/Fichas/Simples/ficha-azul.png"),
            "rojo_doble":       QPixmap("Sprites/Fichas/Dobles/fichas-rojas.png"),
            "amarillo_doble":   QPixmap("Sprites/Fichas/Dobles/fichas-amarillas.png"),
            "verde_doble":      QPixmap("Sprites/Fichas/Dobles/fichas-verdes.png"),
            "azul_doble":       QPixmap("Sprites/Fichas/Dobles/fichas-azules.png")
        }

        self.tarjetas_usuarios = []

    def init_gui(self, usuarios: list):
        self.tablero = QLabel(self)
        self.tablero.setPixmap(self.pixmaps["tablero"])

        self.dado = QLabel(self)
        self.dado.setPixmap(self.pixmaps["dado"])

        self.label_numero = QLabel("", self)

        self.boton_dado = QPushButton("Tirar dado", self)

        self.label_turno = QLabel("Jugador de turno: ?", self)

        # VL texto y boton dado
        vl1 = QVBoxLayout(self)
        vl1.addWidget(self.boton_dado)
        vl1.addWidget(self.label_numero)

        # HL dado
        hl1 = QHBoxLayout()
        hl1.addStretch(1)
        hl1.addWidget(self.dado)
        hl1.addLayout(vl1)
        hl1.addStretch(1)

        # VL dado y tablero
        vl2 = QVBoxLayout()
        vl2.addStretch(1)
        vl2.addWidget(self.tablero)
        vl2.addStretch(1)
        vl2.addLayout(hl1)
        vl2.addStretch(1)

        # VL usuarios
        self.vl3 = QVBoxLayout()
        self.vl3.addWidget(self.label_turno)
        self.cargar_usuarios(usuarios)

        # HL global
        hl2 = QHBoxLayout()
        hl2.addLayout(vl2)
        hl2.addLayout(self.vl3)

        self.setLayout(hl2)

        self.mostrar()

    def cargar_usuarios(self, usuarios: list):
        num = self.vl3.count()

        for user in usuarios[num - 1:]:
            icono = QLabel(self)
            icono.setPixmap(self.fichas[user["color"]])

            usuario = user["usuario"]
            label_usuario = QLabel(usuario, self)
            label_turno = QLabel(f"Turno: {usuarios.index(user) + 1}", self)
            label_en_base = QLabel(f"Fichas en base: {2}", self)
            label_en_color = QLabel(f"Fichas en color: {0}", self)
            label_en_victoria = QLabel(f"Fichas en victoria: {0}", self)

            tarjeta = TarjetaUsuario(self, label_usuario, icono, label_turno,
                                     label_en_base, label_en_color, label_en_victoria)

            self.tarjetas_usuarios.append(tarjeta)
            self.vl3.addLayout(tarjeta.layout())

    def mostrar(self):
        self.show()


class TarjetaUsuario:
    def __init__(self, parent, usuario, icono, turno, base, fichas_color, victoria):
        self.parent = parent
        self.label_usuario = usuario
        self.label_icono = icono
        self.label_turno = turno
        self.label_fichas_base = base
        self.label_fichas_color = fichas_color
        self.label_fichas_victoria = victoria

    def layout(self) -> QHBoxLayout:
        # VL datos
        vl1 = QVBoxLayout()
        vl1.addWidget(self.label_usuario)
        vl1.addWidget(self.label_turno)
        vl1.addWidget(self.label_fichas_base)
        vl1.addWidget(self.label_fichas_color)
        vl1.addWidget(self.label_fichas_victoria)

        # HL tarjeta
        hl1 = QHBoxLayout()
        hl1.addWidget(self.label_icono)
        hl1.addLayout(vl1)
        hl1.addStretch(1)

        return hl1
