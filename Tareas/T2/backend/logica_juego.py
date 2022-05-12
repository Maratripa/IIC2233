from os import path
from collections import deque
from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QThread, QUrl
from PyQt5.QtMultimedia import QSound, QSoundEffect
from backend.entidades import Mira, Alien

import parametros as p


class Juego(QObject):
    #                               (niv, esc, bal, tiemp, pos_mira)
    senal_iniciar_juego = pyqtSignal(int, int, int, float, tuple)
    #                             (id , x  , y  , w  , h  , senales)
    senal_crear_aliens = pyqtSignal(int, int, int, int, int, list)

    senal_actualizar_tiempo = pyqtSignal(int)

    senal_actualizar_balas = pyqtSignal(int)

    senal_actualizar_puntaje = pyqtSignal(int)

    senal_terminar_nivel = pyqtSignal(int, int, int, int, int, int, bool)

    senal_esconder_ventana_juego = pyqtSignal()

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

        self.explotador = Explosion(self)

        # Aliens
        self.aliens = {}
        self.rapidez_aliens = p.VELOCIDAD_ALIEN[0] + p.VELOCIDAD_ALIEN[1]
        self.aliens_vivos = set()
        self.aliens_muertos = set()
        self.aliens_por_eliminar = []

        # Juego
        self.cantidad_aliens = 2

        self.tiempo = p.DURACION_NIVEL_INICIAL  # msecs

        self.timer_tiempo = Tiempo(self)
        self.timer_tiempo.setSingleShot(True)
        self.timer_tiempo.timeout.connect(
            lambda: self.terminar_nivel(False)
        )

    def iniciar_juego(self, escenario, usuario):
        self.escenario = escenario
        self.usuario = usuario

        self.iniciar_nivel(1)

    def iniciar_nivel(self, nivel: int) -> None:
        self.nivel = nivel

        self.mira.x, self.mira.y = (p.VENTANA_ANCHO / 2 - p.ANCHO_MIRA / 2,
                                    p.VENTANA_ALTO / 2 - p.ALTO_MIRA / 2)

        self.timer_tiempo.setInterval(self.tiempo)
        self.cantidad_aliens = nivel * 2
        self.balas = self.cantidad_aliens * 2
        self.aliens_muertos = set()
        self.aliens_vivos = set()
        self.teclas = set()
        self.senal_iniciar_juego.emit(nivel, self.escenario, self.balas,
                                      self.tiempo, (self.mira.x, self.mira.y))
        self.timer.start()
        self.timer_tiempo.start()

    def actualizar_juego(self):
        if not self.pausa:
            self.mira.actualizar(self.teclas)
            self.manejar_aliens()

            self.senal_actualizar_tiempo.emit(self.timer_tiempo.remainingTime())

    def manejar_aliens(self):
        # Crear mientras falten aliens por matar
        if len(self.aliens_vivos) == 0 and len(self.aliens_muertos) != self.cantidad_aliens:
            self.crear_aliens()

        # Eliminar todos los aliens en la lista
        for i in range(len(self.aliens_por_eliminar) - 1, -1, -1):
            del self.aliens[self.aliens_por_eliminar.pop(i)]

        # Mover aliens
        for id in self.aliens:
            self.aliens[id].mover()

    def crear_aliens(self):
        for _ in range(2):
            alien = Alien(self.escenario, self.rapidez_aliens)
            self.aliens[alien.id] = alien
            self.aliens_vivos.add(alien.id)
            self.senal_crear_aliens.emit(
                alien.id, alien.x, alien.y, alien.width, alien.height,
                [alien.senal_posicion, alien.senal_morir, alien.senal_eliminar])
            alien.senal_eliminar.connect(self.eliminar_alien)

    def eliminar_alien(self, id: int):
        self.aliens_por_eliminar.append(id)

        # Terminar juego cuando el ultimo alien salga de la pantalla
        if len(self.aliens_muertos) == self.cantidad_aliens and self.ultimo_disparado == id:
            self.terminar_nivel(True)
            self.timer_tiempo.stop()

    def terminar_nivel(self, paso_nivel: bool):
        self.timer.stop()
        self.senal_esconder_ventana_juego.emit()
        self.senal_terminar_nivel.emit(self.nivel, self.escenario,
                                       self.balas, int(self.timer_tiempo.remainingTime() / 1000),
                                       100, 100, paso_nivel)

    def actualizar_teclas(self, key: int) -> None:
        if key == 78:           # tecla: n
            self.crear_aliens()

        elif key == 80:
            self.pausar_juego()  # tecla: p

        elif key > 0:           # keyPressEvent
            self.teclas.add(key)

        else:                   # keyReleaseEvent
            self.teclas.discard(-key)

    def disparar(self, disparando: bool):
        if disparando:
            self.balas -= 1
            self.senal_actualizar_balas.emit(self.balas)
            self.sonido_disparo.play()
            chocados = self.chequear_colision_aliens()

            if chocados:
                self.crear_explosion(self.mira.x + self.mira.off_w,
                                     self.mira.y + self.mira.off_h)
                for id in chocados:
                    self.aliens[id].morir()
                    self.aliens_vivos.remove(id)
                    self.aliens_muertos.add(id)
                    self.ultimo_disparado = id

            if self.balas == 0 and len(self.aliens_muertos) != self.cantidad_aliens:
                self.terminar_nivel(False)
                self.timer_tiempo.stop()

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

    def crear_explosion(self, x, y):
        self.explotador.mover_explosion(x, y)
        self.explotador.start()

    def pausar_juego(self):
        self.pausa = not self.pausa
        if self.pausa:
            self.timer_tiempo.pausa()
        else:
            self.timer_tiempo.reanudar()


class Explosion(QThread):
    #                           (fase)
    senal_explosion = pyqtSignal(int)
    #                       (x  , y  )
    senal_mover = pyqtSignal(int, int)

    def __init__(self, parent):
        super().__init__(parent)

        self.time_off = 75

    # Explosion en un nuevo lugar
    def mover_explosion(self, x, y):
        self.senal_mover.emit(x, y)

    def run(self):
        """

        """
        self.senal_explosion.emit(0)
        self.msleep(self.time_off)
        self.senal_explosion.emit(1)
        self.msleep(self.time_off)
        self.senal_explosion.emit(2)
        self.msleep(self.time_off)
        self.senal_explosion.emit(-1)


class Tiempo(QTimer):
    def __init__(self, parent):
        super().__init__(parent)

    def pausa(self):
        self.restante = self.remainingTime()
        self.stop()

    def reanudar(self):
        self.setInterval(self.restante)
        self.start()
