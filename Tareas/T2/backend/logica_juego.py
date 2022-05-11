from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from backend.entidades import Mira, Alien

import parametros as p


class Juego(QObject):
    #                               (pos_mira)
    senal_iniciar_juego = pyqtSignal(tuple)
    #                             (id , x  , y  , w  , h  , senales)
    senal_crear_alien = pyqtSignal(int, int, int, int, int, list)

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
            chocados = self.chequear_colision_aliens()

            if chocados:
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
