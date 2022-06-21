from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5.QtGui import QPixmap

from utils import data_json, posicion_ficha, posicion_estrella


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

        self.tamano_estrella = data_json("TAMANO_ESTRELLA")

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

        self.tarjetas_usuarios = {}

        self.estrellas = {}

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
        self.vl3_1 = QVBoxLayout()

        # VL usuarios y turno
        self.vl3 = QVBoxLayout()
        self.vl3.setSpacing(10)
        self.vl3.addLayout(hl1_1)
        self.vl3.addStretch(1)
        self.vl3.addLayout(self.vl3_1)
        self.vl3.addStretch(1)


        # HL global
        hl2 = QHBoxLayout()
        hl2.addLayout(vl2)
        hl2.addLayout(self.vl3)

        self.setLayout(hl2)

    def cargar_usuarios(self, usuarios: list):
        for key in self.fichas.keys():
            self.fichas[key].hide()
            self.fichas[key].setParent(None)
        
        self.fichas = {}
        
        for key in self.estrellas.keys():
            self.estrellas[key].hide()
            self.estrellas[key].setParent(None)
        
        self.estrellas = {}

        for key in self.tarjetas_usuarios.keys():
            self.tarjetas_usuarios[key].hide()
            self.tarjetas_usuarios[key].setParent(None)
        
        self.tarjetas_usuarios = {}

        tamano_ficha = data_json("TAMANO_FICHA")

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

            self.tarjetas_usuarios[user['color']] = tarjeta
            self.vl3_1.addWidget(tarjeta.layout())

            label_ficha = QLabel(self)
            label_ficha.setPixmap(self.pixmap_fichas[user['color']])
            label_ficha.setFixedSize(tamano_ficha, tamano_ficha)

            label_segunda_ficha = QLabel(self)
            label_segunda_ficha.setPixmap(self.pixmap_fichas[user['color']])
            label_segunda_ficha.setFixedSize(tamano_ficha, tamano_ficha)
            label_segunda_ficha.stackUnder(label_ficha)

            self.fichas[user['color']] = label_ficha
            self.fichas[f"{user['color']}_segunda"] = label_segunda_ficha

            self.estrellas[user['color']] = QLabel(self)
            self.estrellas[user['color']].setPixmap(self.pixmaps["estrella"])
            self.estrellas[user['color']].setFixedSize(self.tamano_estrella, self.tamano_estrella)
            self.estrellas[user['color']].setScaledContents(True)
            self.estrellas[user['color']].move(
                *posicion_estrella(*data_json(f"POS_ESTRELLA_{user['color'].upper()}")))
            self.estrellas[user['color']].stackUnder(label_segunda_ficha)

        self.repaint()
        self.mostrar()

    def actualizar_juego(self, info: dict):
        if info["en_turno"]:
            self.boton_dado.setEnabled(True)
        else:
            self.boton_dado.setEnabled(False)

        self.label_numero.setText(f"Lanzamiento anterior: {info['num_dado']}")
        self.label_turno.setText(f"Jugador de turno: {info['nombre_en_turno']}")

        for key in info['posiciones']:
            pos_ficha = posicion_ficha(*info['posiciones'][key])
            if "segunda" in info.keys():
                if info['segunda'][key]:
                    self.fichas[f"{key}_segunda"].move(*pos_ficha)
                else:
                    self.fichas[key].move(*pos_ficha)
            else:
                self.fichas[f"{key}_segunda"].move(*pos_ficha)
                self.fichas[key].move(*pos_ficha)
        
        for key in info["data"]:
            self.tarjetas_usuarios[key].actualizar_tarjeta(info["data"][key])
    
    def actualizar_jugadores(self, info: dict):
        if info["en_turno"]:
            self.boton_dado.setEnabled(True)
        else:
            self.boton_dado.setEnabled(False)
        
        self.fichas[info['color_eliminado']].hide()
        self.fichas[info['color_eliminado']].setParent(None)
        self.fichas[f"{info['color_eliminado']}_segunda"].hide()
        self.fichas[f"{info['color_eliminado']}_segunda"].setParent(None)
        self.estrellas[info['color_eliminado']].hide()
        self.estrellas[info['color_eliminado']].setParent(None)
        self.tarjetas_usuarios[info['color_eliminado']].hide()
        self.tarjetas_usuarios[info['color_eliminado']].setParent(None)

        self.repaint()

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

        self.frame = QFrame(self.parent)
        self.frame.setLayout(hl1)
        self.frame.setObjectName("tarjeta-usuario-juego")

        return self.frame
    
    def actualizar_tarjeta(self, data: dict):
        self.label_fichas_base.setText(f"Fichas en base: {data['en_base']}")
        self.label_fichas_color.setText(f"Fichas en color: {data['en_color']}")
        self.label_fichas_victoria.setText(f"Fichas en victoria: {data['en_victoria']}")
    
    def hide(self):
        self.frame.hide()

    def setParent(self, parent):
        self.frame.setParent(parent)
