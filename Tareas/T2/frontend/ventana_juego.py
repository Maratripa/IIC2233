import sys
from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QProgressBar)
import parametros as p


class VentanaJuego(QWidget):

    senal_boton_salir = pyqtSignal()
    senal_boton_pausa = pyqtSignal()
    senal_actualizar_teclas = pyqtSignal(int)

    def __init__(self, nivel: int = 1):
        super().__init__()
        self.setFocus()

        self.nivel = nivel

        # Diccionario de aliens
        self.aliens = {}

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO, p.VENTANA_ALTO + 100)
        self.setWindowTitle("A cazar aliens!")
        self.setStyleSheet(
            "font-size: 16px;",
        )
        self.setFixedSize(p.VENTANA_ANCHO, p.VENTANA_ALTO + 100)

        # Fondo
        self.bg = QLabel(self)
        pixmap_bg = QPixmap(path.join(*p.RUTA_FONDO, "Luna.png"))
        self.bg.setPixmap(pixmap_bg.scaled(p.VENTANA_ANCHO, p.VENTANA_POS_Y, 2, 1))
        self.bg.setGeometry(0, 0, 960, 600)

        # Alien pixmaps
        self.pixmap_alien = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{self.nivel}.png"))
        self.pixmap_alien_muerto = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{self.nivel}_dead.png"))

        # Mira
        self.label_mira = QLabel(self)
        self.pixmap_mira = QPixmap(
            path.join(*p.RUTA_MIRA, "Disparador_negro.png"))
        self.pixmap_mira_roja = QPixmap(
            path.join(*p.RUTA_MIRA, "Disparador_rojo.png"))
        self.label_mira.setPixmap(self.pixmap_mira)
        self.label_mira.setGeometry(0, 0, p.ANCHO_MIRA, p.ALTO_MIRA)
        self.label_mira.setScaledContents(True)

        # Barra inferior
        # VBox tiempo
        self.label_tiempo = QLabel("Tiempo", self)
        self.barra_timepo = QProgressBar(self)
        self.barra_timepo.setTextVisible(False)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label_tiempo)
        vbox1.addWidget(self.barra_timepo)

        # VBox balas
        self.label_balas = QLabel("Balas", self)

        self.icono_bala = QLabel(self)
        self.pixmap_bala = QPixmap("frontend/assets/Sprites/Elementos juego/Bala.png")
        self.icono_bala.setPixmap(self.pixmap_bala.scaled(10, 20))

        self.cuenta_balas = QLabel(f"X 0", self)

        hbox0_1 = QHBoxLayout()
        hbox0_1.addWidget(self.icono_bala)
        hbox0_1.addWidget(self.cuenta_balas)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label_balas)
        vbox2.addLayout(hbox0_1)

        # VBox puntaje
        self.label_puntaje = QLabel("Puntaje", self)
        self.cuenta_puntaje = QLabel("0 ptos", self)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label_puntaje)
        vbox3.addWidget(self.cuenta_puntaje)

        # Vbox nivel
        self.label_nivel = QLabel("Nivel", self)
        self.cuenta_nivel = QLabel(f"0", self)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.label_nivel)
        vbox4.addWidget(self.cuenta_nivel)

        # VBox botones
        self.boton_pausa = QPushButton("&Pausa", self)
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.boton_pausa.setFocusPolicy(4)
        self.boton_salir = QPushButton("&Salir", self)
        self.boton_salir.clicked.connect(self.salir_juego)
        self.boton_salir.setFocusPolicy(4)

        vbox5 = QVBoxLayout()
        vbox5.addWidget(self.boton_pausa)
        vbox5.addWidget(self.boton_salir)

        # HBox barra
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox1)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox2)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox3)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox4)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox5)
        hbox2.addStretch(1)

        # VBox global
        label_vacio = QLabel(self)
        label_vacio.setGeometry(0, 0, 960, 600)

        vbox6 = QVBoxLayout()
        vbox6.addWidget(label_vacio)
        vbox6.addLayout(hbox2)

        vbox6.setContentsMargins(11, 11, 11, 20)

        # Setear Layout
        self.setLayout(vbox6)

    def iniciar_nivel(self, pos_mira: tuple):
        self.label_mira.move(*pos_mira)
        self.show()

    def keyPressEvent(self, event):
        #print(event.key(), event.text())
        self.senal_actualizar_teclas.emit(event.key())

    def keyReleaseEvent(self, event):
        self.senal_actualizar_teclas.emit(-event.key())

    def agregar_label_alien(self, id, x, y, ancho, alto, senal_posicion):
        label = QLabel(self)
        label.setPixmap(self.pixmap_alien)
        label.setGeometry(x, y, ancho, alto)
        label.setScaledContents(True)
        self.aliens[id] = label
        label.show()

        senal_posicion[0].connect(self.mover_alien)

    def mover_alien(self, id: int, pos: tuple):
        self.aliens[id].move(*pos)

    def mover_mira(self, pos: tuple):
        self.label_mira.move(*pos)

    def cambiar_mira(self, disparando: bool):
        if disparando:
            self.label_mira.setPixmap(self.pixmap_mira_roja)
        else:
            self.label_mira.setPixmap(self.pixmap_mira)

    def salir_juego(self):
        self.senal_boton_salir.emit()

    def pausar_juego(self):
        self.senal_boton_pausa.emit()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaJuego("assets/Sprites/Fondos/Galaxia.png", 1, 60, 100)
    sys.exit(app.exec_())
