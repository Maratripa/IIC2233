import math
import random

from PyQt5.QtCore import QTimer, QObject, pyqtSignal

import parametros as p


class Mira(QObject):
    #                          (pos_m)
    senal_posicion = pyqtSignal(tuple)
    senal_disparando = pyqtSignal()

    def __init__(self, width: int, height: int, pos: tuple) -> None:
        super().__init__()

        self.width = width
        self.height = height

        self.off_w = int(self.width / 2)
        self.off_h = int(self.height / 2)

        self._x, self._y = pos

        self.recargando = False

        self.timer_disparo = QTimer(self)
        self.timer_disparo.setInterval(1000)
        self.timer_disparo.setSingleShot(True)
        self.timer_disparo.timeout.connect(self.reset_disparo)

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

    def actualizar(self, teclas: set) -> None:
        if 32 in teclas:
            self.disparar()
        self.mover(teclas)

    def disparar(self) -> None:
        if not self.recargando:
            self.recargando = True
            self.timer_disparo.start()
            self.senal_disparando.emit()

    def mover(self, teclas: set) -> None:
        dx = 0
        dy = 0

        if 87 in teclas:
            dy -= 1
        if 83 in teclas:
            dy += 1
        if 65 in teclas:
            dx -= 1
        if 68 in teclas:
            dx += 1

        norma = math.sqrt(dx ** 2 + dy ** 2)
        if norma != 0:
            self.x += int(p.RAPIDEZ_MIRA * dx / norma)
            self.y += int(p.RAPIDEZ_MIRA * dy / norma)

            self.senal_posicion.emit((self.x, self.y))

    def balas_infinitas(self):
        self.timer_disparo.setInterval(500)

    def reset_disparo(self):
        self.recargando = False


class Alien(QObject):

    id = 0
    #                          (id , pos_a)
    senal_posicion = pyqtSignal(int, tuple)
    #                       (id )
    senal_morir = pyqtSignal(int)
    #                          (id )
    senal_eliminar = pyqtSignal(int)

    def __init__(self, escenario: int, rapidez, lado_pantalla):
        super().__init__()

        self.id += 1
        Alien.id += 1

        self.width = p.ANCHO_ALIEN[escenario - 1]
        self.height = p.ALTO_ALIEN

        self.rapidez = rapidez

        angulo = random.uniform(math.pi / 6, math.pi / 3)
        self.vx = math.cos(angulo) * self.rapidez * random.choice([-1, 1])
        self.vy = math.sin(angulo) * self.rapidez * random.choice([-1, 1])

        if lado_pantalla == 0:
            self._x = random.randint(0, p.VENTANA_ANCHO / 2 - self.width)
        else:
            self._x = random.randint(p.VENTANA_ANCHO / 2, p.VENTANA_ANCHO - self.width)

        self._y = random.randint(0, p.VENTANA_ALTO - self.height)

        self.muerto = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < 0:
            self._x = 0
            self.vx *= -1
        elif value > p.VENTANA_ANCHO - self.width:
            self._x = p.VENTANA_ANCHO - self.width
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
        elif value > p.VENTANA_ALTO - self.height and not self.muerto:
            self._y = p.VENTANA_ALTO - self.height
            self.vy *= -1
        else:
            self._y = value

    def mover(self) -> None:
        if not self.muerto:
            self.x += int(self.vx)
            self.y += int(self.vy)
            self.senal_posicion.emit(self.id, (self.x, self.y))
        else:
            self.mover_abajo()

    def morir(self):
        self.senal_morir.emit(self.id)
        self.muerto = True
        self.vy = self.rapidez

    def mover_abajo(self):
        self.y += self.vy
        if self.y > p.VENTANA_ALTO:
            self.senal_eliminar.emit(self.id)
        else:
            self.vy += p.GRAVEDAD
            self.senal_posicion.emit(self.id, (self.x, self.y))
