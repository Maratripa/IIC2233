import math
import random

from PyQt5.QtCore import QThread, QObject, pyqtSignal

import parametros as p


class Mira(QObject):
    #                          (x  , y  )
    senal_posicion = pyqtSignal(int, int)

    def __init__(self, width: int, height: int, pos: tuple) -> None:
        super().__init__()

        self.width = width
        self.height = height

        self.off_w = int(self.width / 2)
        self.off_h = int(self.height / 2)

        self._x, self._y = pos

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, value) -> None:
        if value < -self.off_w:
            self._x = -self.off_w
        elif value > p.VENTANA_ANCHO - self.off_w:
            self._x = p.VENTANA_ANCHO - self.off_w
        else:
            self._x = value

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, value) -> None:
        if value < -self.off_h:
            self._y = -self.off_h
        elif value > p.VENTANA_ALTO - self.off_h:
            self._y = p.VENTANA_ALTO - self.off_h
        else:
            self._y = value

    def mover(self, teclas: set) -> None:
        dx = 0
        dy = 0

        if 'w' in teclas:
            dy -= 1
        if 's' in teclas:
            dy += 1
        if 'a' in teclas:
            dx -= 1
        if 'd' in teclas:
            dx += 1

        norma = math.sqrt(dx ** 2 + dy ** 2)
        if norma != 0:
            self.x += int(p.RAPIDEZ_MIRA * dx / norma)
            self.y += int(p.RAPIDEZ_MIRA * dy / norma)

            self.senal_posicion.emit(self.x, self.y)


class Alien(QObject):

    id = 0
    #                          (x  , y  )
    senal_posicion = pyqtSignal(int, int)

    def __init__(self, width: int, height: int, rapidez: int):
        super().__init__()

        self.id += 1
        Alien.id += 1

        self.width = width
        self.height = height

        angulo = random.uniform(-math.pi, math.pi)
        self.vx = math.cos(angulo) * rapidez
        self.vy = math.sin(angulo) * rapidez

        self._x = random.randint(0, p.VENTANA_ANCHO - self.width)
        self._y = random.randint(0, p.VENTANA_ALTO - self.height)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < 0:
            self._x = 0
            self.vx *= -1
        elif value > p.VENTANA_ANCHO - self.width:
            self._x = p.VENTANA_ALTO - self.width
            self.vx *= -1
        else:
            self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value < 0:
            self._y = 0
            self.vy *= -1
        elif value > p.VENTANA_ALTO - self.height:
            self._y = p.VENTANA_ALTO - self.height
            self.vy *= -1
        else:
            self._y = value

    def mover(self) -> None:
        self.x += int(self.vx)
        self.y += int(self.vy)

        self.senal_posicion.emit(self.x, self.y)
