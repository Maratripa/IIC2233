import sys
from os import path

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLabel,
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
        self.setFixedSize(p.VENTANA_ANCHO, p.VENTANA_ALTO + 100)

        # Fondo
        self.bg = QLabel(self)
        pixmap_bg = QPixmap(path.join(*p.RUTA_FONDO, "Luna.png"))
        self.bg.setPixmap(pixmap_bg.scaled(p.VENTANA_ANCHO, p.VENTANA_POS_Y, 2, 1))
        self.bg.setGeometry(0, 0, 960, 600)

        self.barra_inferior = QLabel(self)
        self.barra_inferior.setGeometry(0, 600, p.VENTANA_ANCHO, 100)

        # Alien pixmaps
        self.pixmap_alien = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{self.nivel}.png"))
        self.pixmap_alien_muerto = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{self.nivel}_dead.png"))

        # Mira
        self.label_mira = QLabel(self)
        self.label_mira.setObjectName("sprite")
        self.pixmap_mira = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparador_negro.png"))
        self.pixmap_mira_roja = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparador_rojo.png"))
        self.label_mira.setPixmap(self.pixmap_mira)
        self.label_mira.setGeometry(0, 0, p.ANCHO_MIRA, p.ALTO_MIRA)
        self.label_mira.setScaledContents(True)
        self.label_mira.stackUnder(self.barra_inferior)

        # Explosion
        self.label_explosion = QLabel(self)
        self.label_explosion.setObjectName("sprite")
        self.label_explosion.stackUnder(self.label_mira)
        self.label_explosion.setScaledContents(True)
        self.label_explosion.hide()

        self.label_explosion.posicion = (0, 0)

        self.pixmap_explosiones = []
        for i in range(3):
            self.pixmap_explosiones.append(
                QPixmap(path.join(*p.RUTA_ELEMENTOS, f"Disparo_f{i + 1}.png")))
        

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
        self.pixmap_bala = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Bala.png"))
        self.icono_bala.setPixmap(self.pixmap_bala.scaled(20, 40, 1, 1))

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
        self.boton_pausa = QPushButton("Pausa", self)
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.boton_pausa.setFocusPolicy(4)
        self.boton_salir = QPushButton("Salir", self)
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
        label_vacio.setObjectName("vacio")
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
        # print(event.key(), event.text())
        self.senal_actualizar_teclas.emit(event.key())

    def keyReleaseEvent(self, event):
        self.senal_actualizar_teclas.emit(-event.key())

    def agregar_label_alien(self, id, x, y, ancho, alto, senales):
        label = QLabel(self)
        label.setObjectName("sprite")
        label.setPixmap(self.pixmap_alien)
        label.setGeometry(x, y, ancho, alto)
        label.setScaledContents(True)
        label.stackUnder(self.label_explosion)
        self.aliens[id] = label
        label.show()

        senales[0].connect(self.mover_alien)
        senales[1].connect(self.matar_alien)
        senales[2].connect(self.eliminar_alien)

    def mover_alien(self, id: int, pos: tuple):
        self.aliens[id].move(*pos)

    def matar_alien(self, id: int):
        self.aliens[id].setPixmap(self.pixmap_alien_muerto)

    def eliminar_alien(self, id: int):
        self.aliens[id].hide()
        del self.aliens[id]

    def mover_mira(self, pos: tuple):
        self.label_mira.move(*pos)

    def cambiar_mira(self, disparando: bool):
        if disparando:
            self.label_mira.setPixmap(self.pixmap_mira_roja)
        else:
            self.label_mira.setPixmap(self.pixmap_mira)
    
    def mover_explosion(self, x, y):
        self.label_explosion.posicion = (x, y)
    
    def explosion(self, fase):
        self.label_explosion.setPixmap(self.pixmap_explosiones[fase])

        x, y = self.label_explosion.posicion
        self.label_explosion.setGeometry(x - p.ANCHO_EXPLOSION[fase] / 2, 
                                         y - p.ALTO_EXPLOSION[fase] / 2, 
                                         p.ANCHO_EXPLOSION[fase], p.ALTO_EXPLOSION[fase])
        if fase == 0:
            self.label_explosion.show()
        elif fase == -1:
            self.label_explosion.hide()
    def salir_juego(self):
        self.senal_boton_salir.emit()
        self.close()

    def pausar_juego(self):
        self.senal_boton_pausa.emit()
