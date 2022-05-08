"""
Para el correcto funcionamiento, la capeta 'Sprites' debe
ser colocada dentro de frontend/assets.

Muchos de los valores estan hardcodeados a proposito, ya que el manejo de
anchos y altos de sprites los manejare de menor manera despues
"""


from random import randint, uniform
import math
import sys
from PyQt5.QtCore import pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton)
import parametros as p


class Mira():
    def __init__(self, width, height, senal_posicion) -> None:

        self.width = width
        self.height = height

        self.off_w = int(width / 2)
        self.off_h = int(height / 2)

        self._x = int(728 / 2 - self.off_w)
        self._y = int(410 / 2 - self.off_h)

        self.senal_posicion = senal_posicion

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < -self.off_w:
            self._x = -self.off_w
        elif value + self.off_w > 728:
            self._x = 728 - self.off_w
        else:
            self._x = value
        self.senal_posicion.emit(self.x, self.y)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if value < -self.off_h:
            self._y = -self.off_h
        elif value + self.off_h > 410:
            self._y = 410 - self.off_h
        else:
            self._y = value
        self.senal_posicion.emit(self.x, self.y)

    def mover(self, teclas: str) -> None:
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
            self.x += int(dx * p.RAPIDEZ_MIRA / norma)
            self.y += int(dy * p.RAPIDEZ_MIRA / norma)


class Alien(QObject):
    def __init__(self, width, height, senal_posicion):
        super().__init__()

        self.width = width
        self.height = height

        self._x = randint(0, 728 - self.width)
        self._y = randint(0, 410 - self.height)

        angle = uniform(-math.pi, math.pi)
        self.vx = math.cos(angle) * p.RAPIDEZ_ALIEN
        self.vy = math.sin(angle) * p.RAPIDEZ_ALIEN

        self.senal_posicion = senal_posicion

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        if value < 0:
            self._x = 0
            self.vx *= -1
        elif value > 728 - self.width:
            self._x = 728 - self.width
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
        elif value > 410 - self.height:
            self._y = 410 - self.height
            self.vy *= -1
        else:
            self._y = value

    def move(self):
        self.x += int(self.vx)
        self.y += int(self.vy)
        self.senal_posicion.emit(self.x, self.y)


class Juego(QObject):
    def __init__(self, senal_teclas, senal_mover_mira, senal_mover_alien, senal_iniciar):
        super().__init__()

        senal_teclas.connect(self.actualizar_teclas)
        self.senal_iniciar = senal_iniciar

        self.teclas = set()

        self.timer = QTimer(self)
        self.timer.setInterval(p.FRAME_TIME_MS)
        self.timer.timeout.connect(self.update_game)
        self.timer.start()

        self.mira = Mira(240, 160, senal_mover_mira)
        self.alien = Alien(68, 75, senal_mover_alien)

    def iniciar_juego(self):
        self.senal_iniciar.emit(self.mira.x, self.mira.y,
                                self.alien.x, self.alien.y)

    def update_game(self):
        self.mira.mover(self.teclas)
        self.alien.move()

    def actualizar_teclas(self, teclas):
        self.teclas = teclas


class Ventana(QWidget):

    senal_teclas = pyqtSignal(set)
    #                           (x, y)
    mover_jugador = pyqtSignal(int, int)
    #                         (x, y)
    mover_alien = pyqtSignal(int, int)
    #                   (x_mira, y_mira, x_alien, y_alien)
    iniciar_juego = pyqtSignal(int, int, int, int)

    def __init__(self) -> None:
        super().__init__()
        self.iniciar_juego.connect(self.iniciar)

        self.keys_pressed = set()

        self.setWindowTitle("A cazar aliens!")

        self.mover_jugador.connect(self.actualizar_mira)
        self.mover_alien.connect(self.actualizar_alien)

        self.background = QLabel(self)
        bg_pmap = QPixmap("frontend/assets/Sprites/Fondos/Galaxia.png")
        self.background.setPixmap(bg_pmap)

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y,
                         bg_pmap.width(), bg_pmap.height())

        self.label_alien = QLabel(self)
        self.pixmap_alien = QPixmap(
            "frontend/assets/Sprites/Aliens/Alien1.png")

        self.label_alien.setPixmap(self.pixmap_alien.scaled(75, 75, 1, 1))
        self.label_alien.setScaledContents(True)

        self.label_mira = QLabel(self)
        self.pixmap_mira = QPixmap(
            "frontend/assets/Sprites/Elementos juego/Disparador_negro.png")

        self.label_mira.setPixmap(self.pixmap_mira.scaled(240, 160, 1, 1))
        self.label_mira.setScaledContents(True)

        self.backend = Juego(
            self.senal_teclas,
            self.mover_jugador,
            self.mover_alien,
            self.iniciar_juego)

        self.backend.iniciar_juego()

    def iniciar(self, mira_x, mira_y, alien_x, alien_y):
        self.label_mira.move(mira_x, mira_y)
        self.label_alien.move(alien_x, alien_y)

    def keyPressEvent(self, event):
        self.keys_pressed.add(event.text())
        self.senal_teclas.emit(self.keys_pressed)

    def keyReleaseEvent(self, event):
        self.keys_pressed.remove(event.text())
        self.senal_teclas.emit(self.keys_pressed)

    def actualizar_mira(self, x, y):
        self.label_mira.move(x, y)

    def actualizar_alien(self, x, y):
        self.label_alien.move(x, y)


if __name__ == "__main__":
    app = QApplication([])
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec_())
