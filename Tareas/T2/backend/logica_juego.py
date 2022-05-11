from os import path
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
from backend.entidades import Mira, Alien

import parametros as p


class Juego(QObject):
    #                               (pos_mira)
    senal_iniciar_juego = pyqtSignal(tuple)
    #                             (id , x  , y  , w  , h  , senales)
    senal_crear_alien = pyqtSignal(int, int, int, int, int, list)
    #                                 (x  , y  , fase)
    senal_crear_explosion = pyqtSignal(int, int, int)

    def __init__(self):
        super().__init__()

        # Timer para framerate
        self.timer = QTimer()
        self.timer.setInterval(p.FRAME_TIME_MS)
        self.timer.timeout.connect(self.actualizar_juego)

        # Teclas apretadas
        self.teclas = set()

        # Estado de pausa
        self.pausa = False

        # Mira
        self.mira = Mira(p.ANCHO_MIRA, p.ALTO_MIRA, (p.VENTANA_ANCHO / 2 - p.ANCHO_MIRA / 2,
                                                     p.VENTANA_ALTO / 2 - p.ALTO_MIRA / 2))

        self.sonido_disparo = QSoundEffect(self)
        self.sonido_disparo.setSource(QUrl.fromLocalFile(path.join(*p.RUTA_SONIDOS, "disparo.wav")))
        self.sonido_disparo.setVolume(0.3)

        # Aliens
        self.aliens = {}

        self.aliens_por_eliminar = []

    def actualizar_teclas(self, key: int) -> None:
        if key == 78:           # tecla: n
            self.crear_alien()

        elif key > 0:           # keyPressEvent
            self.teclas.add(key)

        else:                   # keyReleaseEvent
            self.teclas.discard(-key)

    def disparar(self, disparando: bool):
        if disparando:
            self.sonido_disparo.play()
            chocados = self.chequear_colision_aliens()

            if chocados:
                self.crear_explosion(self.mira.x + self.mira.off_w, 
                                     self.mira.y + self.mira.off_h)
                for id in chocados:
                    self.aliens[id].morir()

    def chequear_colision_aliens(self) -> list:
        chocados = []
        for id in self.aliens:
            alien = self.aliens[id]
            xm = self.mira.x + self.mira.off_w
            ym = self.mira.y + self.mira.off_h

            colision_x = xm > alien.x and xm < alien.x + alien.width
            colision_y = ym > alien.y and ym < alien.y + alien.height

            if colision_x and colision_y:
                chocados.append(id)

        return chocados

    def crear_alien(self):
        alien = Alien()
        self.aliens[alien.id] = alien
        self.senal_crear_alien.emit(
            alien.id, alien.x, alien.y, alien.width, alien.height,
            [alien.senal_posicion, alien.senal_morir, alien.senal_eliminar])
        alien.senal_eliminar.connect(self.eliminar_alien)

    def eliminar_alien(self, id: int):
        self.aliens_por_eliminar.append(id)

    def crear_explosion(self, x, y):
        explosion = Explosion(x, y, self)
        explosion.senal_explosion.connect(
            lambda x, y, fase: self.senal_crear_explosion.emit(x, y, fase))

    def iniciar_nivel(self, nivel: int, usuario: str) -> None:
        self.senal_iniciar_juego.emit((self.mira.x, self.mira.y))
        self.timer.start()

    def actualizar_juego(self):
        if not self.pausa:
            self.mira.actualizar(self.teclas)
            if self.aliens_por_eliminar:
                del self.aliens[self.aliens_por_eliminar.pop(0)]

            for id in self.aliens:
                if not self.aliens[id].muerto:
                    self.aliens[id].mover()
                else:
                    self.aliens[id].mover_abajo()


class Explosion(QThread):
    #                           (x  , y  , fase)
    senal_explosion = pyqtSignal(int, int, int)

    def __init__(self, x, y, parent):
        super().__init__(parent)

        self.x = x
        self.y = y

        self.time_off = 75

        self.start()

    def run(self):
        """

        """
        self.senal_explosion.emit(self.x, self.y, 0)
        self.msleep(self.time_off)
        self.senal_explosion.emit(self.x, self.y, 1)
        self.msleep(self.time_off)
        self.senal_explosion.emit(self.x, self.y, 2)
        self.msleep(self.time_off)
        self.senal_explosion.emit(self.x, self.y, -1)
