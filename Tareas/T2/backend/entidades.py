import math
import random

from PyQt5.QtCore import QTimer, QObject, pyqtSignal, QThread

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

        # Tiempo entre disparos
        self.timer_disparo = QTimer(self)
        self.timer_disparo.setInterval(p.TIEMPO_RECARGA_NORMAL)
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

    # Mover y disparar
    def actualizar(self, teclas: set) -> None:
        if 32 in teclas:
            self.disparar()
        self.mover(teclas)

    # Disparar si no esta recargando
    def disparar(self) -> None:
        if not self.recargando:
            self.recargando = True
            self.timer_disparo.start()
            self.senal_disparando.emit()

    # Mover en 4 direcciones + diagonales normalizadas
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

    # Cheat code balas infinitas
    def balas_infinitas(self):
        self.timer_disparo.setInterval(p.TIEMPO_RECARGA_SUPER)

    # Puede volver a disparar
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

        # Crear id ??nica de alien
        self.id += 1
        Alien.id += 1

        self.width = p.ANCHO_ALIEN[escenario - 1]
        self.height = p.ALTO_ALIEN

        self.rapidez = rapidez

        # Velocidad en ??ngulo random pero siempre diagonal en cierto grado
        angulo = random.uniform(math.pi / 6, math.pi / 3)
        self.vx = math.cos(angulo) * self.rapidez * random.choice([-1, 1])
        self.vy = math.sin(angulo) * self.rapidez * random.choice([-1, 1])

        # Evitar superposicion al instanciarse
        if lado_pantalla == 0:
            self._x = random.randint(0, p.VENTANA_ANCHO / 2 - self.width)
        else:
            self._x = random.randint(p.VENTANA_ANCHO / 2, p.VENTANA_ANCHO - self.width)

        self._y = random.randint(0, p.VENTANA_ALTO - self.height)

        # Variable para eliminar alien
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

    # Moverse
    def mover(self) -> None:
        if not self.muerto:
            self.x += int(self.vx)
            self.y += int(self.vy)
            self.senal_posicion.emit(self.id, (self.x, self.y))
        else:
            self.mover_abajo()

    # Enviar se??al de muerto y moverse hacia abajo
    def morir(self):
        self.senal_morir.emit(self.id)
        self.muerto = True
        self.vy = self.rapidez

    # Moverse hacia abajo una vez muerto
    def mover_abajo(self):
        self.y += self.vy
        if self.y > p.VENTANA_ALTO:
            self.senal_eliminar.emit(self.id)
        else:
            self.vy += p.GRAVEDAD
            self.senal_posicion.emit(self.id, (self.x, self.y))


class BombaHielo(QTimer):

    senal_estado_bomba = pyqtSignal(int)
    senal_pos_bomba = pyqtSignal(int, int)

    def __init__(self, parent):
        super().__init__(parent)

        self.width = p.ANCHO_BOMBA
        self.height = p.ALTO_BOMBA

        self.setInterval(p.TIEMPO_BOMBA * 1000)
        self.setSingleShot(True)
        self.timeout.connect(self.esconder)
        self.activa = False

    def partir(self):
        self.x = random.randint(0, p.VENTANA_ANCHO - p.ANCHO_BOMBA)
        self.y = random.randint(0, p.VENTANA_ALTO - p.ALTO_BOMBA)

        self.senal_pos_bomba.emit(self.x, self.y)
        self.senal_estado_bomba.emit(1)
        self.activa = True
        self.start()

    def esconder(self):
        self.activa = False
        self.senal_estado_bomba.emit(-1)


class EstrellaMuerte(QTimer):

    senal_pos_estrella = pyqtSignal(int, int)
    senal_estado_estrella = pyqtSignal(int)

    def __init__(self, parent):
        super().__init__(parent)

        self.width = p.ANCHO_ESTRELLA
        self.height = p.ALTO_ESTRELLA

        self.setInterval(p.TIEMPO_ESTRELLA * 1000)
        self.setSingleShot(True)
        self.timeout.connect(self.esconder)
        self.activa = False

    def spawn(self):
        self.x = random.randint(0, p.VENTANA_ANCHO - self.width)
        self.y = random.randint(0, p.VENTANA_ALTO - self.height)

        self.senal_pos_estrella.emit(self.x, self.y)
        self.senal_estado_estrella.emit(1)
        self.activa = True
        self.start()

    def esconder(self):
        self.activa = False
        self.senal_estado_estrella.emit(-1)


# Clase encargada de mover y generar la explosion
class Explosion(QThread):
    #                           (fase)
    senal_explosion = pyqtSignal(int)
    #                       (x  , y  )
    senal_mover = pyqtSignal(int, int)

    def __init__(self, parent):
        super().__init__(parent)

        self.time_off = p.TIEMPO_OFFSET_EXPLOSION

    # Explosion en un nuevo lugar
    def mover_explosion(self, x, y):
        self.senal_mover.emit(x, y)

    def run(self):
        # Cambiar fase de explosion cada self.time_off msecs
        self.senal_explosion.emit(0)
        self.msleep(self.time_off)
        self.senal_explosion.emit(1)
        self.msleep(self.time_off)
        self.senal_explosion.emit(2)
        self.msleep(self.time_off)
        self.senal_explosion.emit(-1)


# Clase de timer con m??todo reanudar()
class Tiempo(QTimer):
    def __init__(self, parent):
        super().__init__(parent)

    def pausa(self):
        self.restante = self.remainingTime()
        self.stop()

    def reanudar(self):
        self.setInterval(self.restante)
        self.start()
