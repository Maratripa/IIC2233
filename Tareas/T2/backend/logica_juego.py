import os

from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from backend.entidades import Mira, Alien

import parametros as p


class Juego(QObject):

    senal_iniciar_juego = pyqtSignal()

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
        self.mira = None

        # Aliens
        self.aliens = {}  # id: instancia

    def actualizar_teclas(self, teclas: set) -> None:
        self.teclas = teclas

    def iniciar_nivel(self, nivel: int, usuario: str) -> None:
        pass

    def actualizar_juego(self):
        if not self.pausa:
            pass
