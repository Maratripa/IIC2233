from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap

from utils import data_json, posicion_ficha


class VentanaJuego(QWidget):
    #                            (comando)
    senal_tirar_dado = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        ancho_ventana = data_json("ANCHO_VENTANA_JUEGO")
        alto_ventana = data_json("ALTO_VENTANA_JUEGO")
        pos_ventana = data_json("POS_VENTANA")

        self.setGeometry(pos_ventana[0], pos_ventana[1],
                         ancho_ventana,  alto_ventana)
        self.setWindowTitle("DCCasillas")

        ruta_sprites = path.join(*data_json("RUTA_SPRITES"))
        ruta_fichas_simples = path.join(ruta_sprites, "Fichas", "Simples")
        ruta_fichas_dobles = path.join(ruta_sprites, "Fichas", "Dobles")

        self.pixmaps = {
            "tablero":  QPixmap(path.join(ruta_sprites, "Juego", "tablero.png")),
            "dado":     QPixmap(path.join(ruta_sprites, "Logos", "dado.png")),
            "estrella": QPixmap(path.join(ruta_sprites, "Juego", "estrella.png")),
            "logo":     QPixmap(path.join(ruta_sprites, "Logos", "logo.png"))
        }

        self.pixmap_fichas = {
            "rojo":             QPixmap(path.join(ruta_fichas_simples, "ficha-roja.png")),
            "amarillo":         QPixmap(path.join(ruta_fichas_simples, "ficha-amarilla.png")),
            "verde":            QPixmap(path.join(ruta_fichas_simples, "ficha-verde.png")),
            "azul":             QPixmap(path.join(ruta_fichas_simples, "ficha-azul.png")),
            "rojo_doble":       QPixmap(path.join(ruta_fichas_dobles, "fichas-rojas.png")),
            "amarillo_doble":   QPixmap(path.join(ruta_fichas_dobles, "fichas-amarillas.png")),
            "verde_doble":      QPixmap(path.join(ruta_fichas_dobles, "fichas-verdes.png")),
            "azul_doble":       QPixmap(path.join(ruta_fichas_dobles, "fichas-azules.png"))
        }

        self.fichas = {}

        self.tarjetas_usuarios = []

    def init_gui(self, usuarios: list):
        self.tablero = QLabel(self)
        self.tablero.setPixmap(self.pixmaps["tablero"])

        self.dado = QLabel(self)
        self.dado.setFixedSize(data_json("TAMANO_DADO"), data_json("TAMANO_DADO"))
        self.dado.setPixmap(self.pixmaps["dado"])
        self.dado.setScaledContents(True)

        self.label_numero = QLabel("Lanzamiento anterior: ?", self)

        self.boton_dado = QPushButton("Tirar dado", self)
        self.boton_dado.setEnabled(False)  # Boton desabilitado por default
        self.boton_dado.clicked.connect(self.tirar_dado)

        self.label_turno = QLabel("Jugador de turno: ?", self)
        self.label_turno.setObjectName("label-turno")

        # VL texto y boton dado
        vl1 = QVBoxLayout()
        vl1.addWidget(self.boton_dado)
        vl1.addWidget(self.label_numero)

        # HL dado
        hl1 = QHBoxLayout()
        hl1.addStretch(2)
        hl1.addWidget(self.dado)
        hl1.addStretch(1)
        hl1.addLayout(vl1)
        hl1.addStretch(4)

        # VL dado y tablero
        vl2 = QVBoxLayout()
        vl2.addStretch(1)
        vl2.addWidget(self.tablero)
        vl2.addStretch(1)
        vl2.addLayout(hl1)
        vl2.addStretch(1)

        # HL label turno
        hl1_1 = QHBoxLayout()
        hl1_1.addStretch(1)
        hl1_1.addWidget(self.label_turno)
        hl1_1.addStretch(1)

        # VL usuarios
        self.vl3 = QVBoxLayout()
        self.vl3.addLayout(hl1_1)
        self.vl3.addStretch(1)
        self.vl3.addLayout(self.cargar_usuarios(usuarios))
        self.vl3.addStretch(1)

        # HL global
        hl2 = QHBoxLayout()
        hl2.addLayout(vl2)
        hl2.addLayout(self.vl3)

        self.setLayout(hl2)

        self.mostrar()

    def cargar_usuarios(self, usuarios: list) -> QVBoxLayout:
        vl = QVBoxLayout()
        vl.setSpacing(10)

        for user in usuarios:
            icono = QLabel(self)
            icono.setPixmap(self.pixmap_fichas[user["color"]])

            usuario = user["usuario"]
            label_usuario = QLabel(usuario, self)
            label_usuario.setObjectName("label-usuario")
            label_turno = QLabel(f"Turno: {usuarios.index(user) + 1}", self)
            label_en_base = QLabel(f"Fichas en base: {2}", self)
            label_en_color = QLabel(f"Fichas en color: {0}", self)
            label_en_victoria = QLabel(f"Fichas en victoria: {0}", self)

            tarjeta = TarjetaUsuario(self, label_usuario, icono, label_turno,
                                     label_en_base, label_en_color, label_en_victoria)

            self.tarjetas_usuarios.append(tarjeta)
            vl.addWidget(tarjeta.layout())

            label_ficha = QLabel(self)
            label_ficha.setPixmap(self.pixmap_fichas[user['color']])

            self.fichas[user['color']] = label_ficha

        return vl

    def actualizar_juego(self, info: dict):
        if info["en_turno"]:
            self.boton_dado.setEnabled(True)
        else:
            self.boton_dado.setEnabled(False)

        self.label_numero.setText(f"Lanzamiento anterior: {info['num_dado']}")
        self.label_turno.setText(f"Jugador de turno: {info['nombre_en_turno']}")

        for key in info['posiciones']:
            pos_ficha = posicion_ficha(*info['posiciones'][key])
            self.fichas[key].move(*pos_ficha)

    def tirar_dado(self):
        self.senal_tirar_dado.emit({"comando": "tirar_dado"})

    def mostrar(self):
        self.show()

    def esconder(self):
        self.hide()


class TarjetaUsuario:
    def __init__(self, parent, usuario, icono, turno, base, fichas_color, victoria):
        self.parent = parent
        self.label_usuario = usuario
        self.label_icono = icono
        self.label_turno = turno
        self.label_fichas_base = base
        self.label_fichas_color = fichas_color
        self.label_fichas_victoria = victoria

    def layout(self) -> QFrame:
        # VL datos
        vl1 = QVBoxLayout()
        vl1.addStretch(1)
        vl1.addWidget(self.label_turno)
        vl1.addWidget(self.label_fichas_base)
        vl1.addWidget(self.label_fichas_color)
        vl1.addWidget(self.label_fichas_victoria)
        vl1.addStretch(1)

        # VL icono y usuario
        vl2 = QVBoxLayout()
        vl2.addStretch(1)
        vl2.addWidget(self.label_icono)
        vl2.addWidget(self.label_usuario)
        vl2.addStretch(1)

        # HL tarjeta
        hl1 = QHBoxLayout()
        hl1.addLayout(vl2)
        hl1.addStretch(1)
        hl1.addLayout(vl1)
        hl1.addStretch(1)

        frame = QFrame(self.parent)
        frame.setLayout(hl1)
        frame.setObjectName("tarjeta-usuario-juego")

        return frame
