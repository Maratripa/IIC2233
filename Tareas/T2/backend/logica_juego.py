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

    senal_actualizar_balas = pyqtSignal(str)

    senal_actualizar_puntaje = pyqtSignal(int)

    senal_terminar_nivel = pyqtSignal(int, int, int, int, int, int, bool, str)

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
        self.timer_tiempo = Tiempo(self)
        self.timer_tiempo.setSingleShot(True)
        self.timer_tiempo.timeout.connect(
            lambda: self.terminar_nivel(False)
        )

    def iniciar_juego(self, escenario, usuario):
        self.escenario = escenario

        if escenario == 1:
            self.dificultad = p.PONDERADOR_TUTORIAL
        elif escenario == 2:
            self.dificultad = p.PONDERADOR_ENTRENAMIENTO
        elif escenario == 3:
            self.dificultad = p.PONDERADOR_INVASION

        self.usuario = usuario
        self.puntaje = 0

        self.cantidad_aliens = 2
        self.tiempo = p.DURACION_NIVEL_INICIAL  # msecs

        self.iniciar_nivel(1)

    def iniciar_nivel(self, nivel: int) -> None:
        self.nivel = nivel

        self.tiempo *= self.dificultad
        self.rapidez_aliens /= self.dificultad

        self.timer_tiempo.setInterval(self.tiempo)
        self.cantidad_aliens = nivel * 2
        self.balas = self.cantidad_aliens * 2
        self.balas_infinitas = False

        # Resetear sets
        self.aliens_muertos = set()
        self.aliens_vivos = set()
        self.teclas = set()

        self.mira.timer_disparo.setInterval(1000)
        self.mira.x, self.mira.y = (p.VENTANA_ANCHO / 2 - p.ANCHO_MIRA / 2,
                                    p.VENTANA_ALTO / 2 - p.ALTO_MIRA / 2)

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
        for i in range(2):  # Se usa 'i' para indicarle en que mitad de la pantalla aparecer
            alien = Alien(self.escenario, self.rapidez_aliens, i)
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
        tiempo_restante = int(self.timer_tiempo.remainingTime() / 1000)
        self.timer.stop()
        self.senal_esconder_ventana_juego.emit()
        if paso_nivel:
            puntos_nivel = self.calcular_puntaje_nivel(tiempo_restante)
        else:
            puntos_nivel = 0
        self.puntaje += puntos_nivel
        self.senal_terminar_nivel.emit(self.nivel, self.escenario,
                                       self.balas, tiempo_restante,
                                       self.puntaje, puntos_nivel,
                                       paso_nivel, self.usuario)

    def calcular_puntaje_nivel(self, tiempo_restante) -> int:
        pts = int(self.cantidad_aliens * 100 +
                  (tiempo_restante * 30 + self.balas * 70) * self.nivel / self.dificultad)
        return pts

    def actualizar_teclas(self, key: int) -> None:
        if key == 80:           # tecla: p
            self.pausar_juego()

        elif key > 0:           # keyPressEvent
            self.teclas.add(key)

        else:                   # keyReleaseEvent
            self.teclas.discard(-key)

        if {67, 73, 65}.issubset(self.teclas):  # Cheatcode CIA
            self.terminar_nivel(True)
            self.timer_tiempo.stop()

        elif {79, 86, 78, 73}.issubset(self.teclas):  # Cheatcode OVNI
            self.balas_infinitas = True
            self.mira.balas_infinitas()
            self.senal_actualizar_balas.emit("INF")

    def disparar(self):
        if not self.balas_infinitas:
            self.balas -= 1
            self.senal_actualizar_balas.emit(str(self.balas))

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

        # No quedan balas
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
