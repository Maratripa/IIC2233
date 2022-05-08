from random import randint, uniform
import math
import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton)
import parametros as p


class Mira(QObject):
    def __init__(self) -> None:
        super().__init__()

        self.sprite = QPixmap(
            "frontend/assets/Sprites/Elementos\ juego/Disparador_negro.png")
        self.off_w = self.sprite.width() / 2
        self.off_h = self.sprite.height() / 2

        self.pos = (p.VENTANA_ANCHO / 2 - self.off_w,
                    p.VENTANA_ALTO / 2 - self.off_h)

        self.velocidad = (0, 0)

    def mover(self, dir: str) -> None:
        if dir == "U":
            self.velocidad[1] = p.RAPIDEZ_MIRA
        elif dir == "D":
            self.velocidad[1] = -p.RAPIDEZ_MIRA
        else:
            self.velocidad[1] = 0

        if dir == "L":
            self.velocidad[0] = -p.RAPIDEZ_MIRA
        elif dir == "R":
            self.velocidad[0] = p.RAPIDEZ_MIRA
        else:
            self.velocidad[0] = 0

        norma = math.sqrt(self.velocidad[0] ** 2 + self.velocidad[1] ** 2)

        if norma != 0:
            self.velocidad = (self.velocidad[0] / norma,
                              self.velocidad[1] / norma)
            self.pos[0] += self.velocidad[0]
            self.pos[1] += self.velocidad[1]

        if self.pos[0] < -self.off_w:
            self.pos[0] = -self.off_w
        elif self.pos[0] > p.VENTANA_ANCHO - self.off_w:
            self.pos[0] = p.VENTANA_ANCHO - self.off_w

        if self.pos[1] < -self.off_h:
            self.pos[1] = self.off_h
        elif self.pos[1] > p.VENTANA_ALTO - self.off_h:
            self.pos[1] = p.VENTANA_ALTO - self.off_h


class Alien(QObject):
    def __init__(self):
        super().__init__()

        self.sprite = QPixmap(
            "frontend/assets/Sprites/Aliens/Alien1.png")

        self.width = self.sprite.width()
        self.height = self.sprite.height()

        self.pos = (randint(0, p.VENTANA_ANCHO - self.width),
                    randint(0, p.VENTANA_ALTO - self.height))

        angle = uniform(-math.pi, math.pi)
        self.velocidad = (math.cos(angle) * p.RAPIDEZ_ALIEN,
                          math.sen(angle) * p.RAPIDEZ_ALIEN)

    def mover(self):
        self.pos[0] += self.velocidad[0]
        self.pos[1] += self.velocidad[1]

        if self.pos[0] < 0:
            self.pos[0] = 0
            self.velocidad[0] *= -1
        elif self.pos[0] > p.VENTANA_ANCHO - self.width:
            self.pos[0] = p.VENTANA_ANCHO - self.width
            self.velocidad[0] *= -1

        if self.pos[1] < 0:
            self.pos[1] = 0
            self.velocidad[1] *= -1
        elif self.pos[1] > p.VENTANA_ALTO - self.height:
            self.pos[1] = p.VENTANA_ALTO - self.height
            self.velocidad[1] *= -1


class Juego(QObject):
    def __init__(self, senal_tecla):
        pass


class Ventana(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.tecla_apretada = pyqtSignal(str)

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y,
                         p.VENTANA_ANCHO, p.VENTANA_ALTO)
        self.setWindowTitle("A cazar aliens!")
        self.setStyleSheet("background-color: #1A1826;")
        self.crear_elementos()

    def crear_elementos(self) -> None:
        self.background = QLabel(self)
        bg_pmap = QPixmap("frontend/assets/Sprites/Fondos/Galaxia.png")
        self.background.setPixmap(bg_pmap)

    def keyPressEvent(self, event):
        self.tecla_apretada.emit(event.text())
