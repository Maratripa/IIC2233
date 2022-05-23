from os import path

import functools
import random

from PyQt5.QtCore import QObject, pyqtSignal, QTimer, QUrl
from PyQt5.QtMultimedia import QSoundEffect
from backend.entidades import Mira, Alien, BombaHielo, Tiempo, Explosion

from manejo_archivos import guardar_puntaje
import parametros as p


class Juego(QObject):
    #                               (lvl, esc, bls, tiemp, pts, pos_mira)
    senal_iniciar_juego = pyqtSignal(int, int, int, float, int, tuple)
    #                              (id , x  , y  , w  , h  , senales)
    senal_crear_aliens = pyqtSignal(int, int, int, int, int, list)
    #                                   (tmp)
    senal_actualizar_tiempo = pyqtSignal(int)
    #                                  (bls_str)
    senal_actualizar_balas = pyqtSignal(str)
    #                                (paso)
    senal_terminator_god = pyqtSignal(bool)
    #                                (lvl, esc, bls, tmp, ptt, ptn, paso, usr)
    senal_terminar_nivel = pyqtSignal(int, int, int, int, int, int, bool, str)

    senal_esconder_ventana_juego = pyqtSignal()

    def __init__(self):
        super().__init__()

        # Timer para framerate
        self.timer = QTimer(self)
        self.timer.setInterval(p.FRAME_TIME_MS)
        self.timer.timeout.connect(self.actualizar_juego)

        # Timer termino nivel
        self.timer_final = QTimer(self)
        # Multiplicado para pasar segs a msegs
        self.timer_final.setInterval(p.TIEMPO_TERMINATOR_DOG * 1000)
        self.timer_final.setSingleShot(True)

        # Timer juego
        self.timer_tiempo = Tiempo(self)
        self.timer_tiempo.setSingleShot(True)
        callback = functools.partial(self.terminar_nivel, False)
        self.timer_tiempo.timeout.connect(callback)

        # Teclas apretadas
        self.teclas = set()

        # Estado de pausa
        self.pausa = False

        # Mira
        self.mira = Mira(p.ANCHO_MIRA, p.ALTO_MIRA, (p.VENTANA_ANCHO / 2 - p.ANCHO_MIRA / 2,
                                                     p.VENTANA_ALTO / 2 - p.ALTO_MIRA / 2))

        # Efecto de sonido disparo
        self.sonido_disparo = QSoundEffect(self)
        self.sonido_disparo.setSource(QUrl.fromLocalFile(path.join(*p.RUTA_SONIDOS, "disparo.wav")))
        self.sonido_disparo.setVolume(0.3)

        # Sonido risa god
        self.sonido_risa = QSoundEffect(self)
        self.sonido_risa.setSource(QUrl.fromLocalFile(
            path.join(*p.RUTA_SONIDOS, "risa_robotica.wav")))
        self.sonido_risa.setVolume(0.3)

        # Case para manejar explosion
        self.explotador = Explosion(self)

        # Aliens
        self.aliens = {}
        self.rapidez_aliens = p.VELOCIDAD_ALIEN[0] + p.VELOCIDAD_ALIEN[1]
        self.aliens_vivos = set()
        self.aliens_muertos = set()
        self.aliens_por_eliminar = []

        # BONUS
        self.bomba_hielo = BombaHielo(self)
        self.congelado = False
        self.timer_congelado = QTimer(self)
        self.timer_congelado.setInterval(p.TIEMPO_CONGELAMIENTO * 1000)
        self.timer_congelado.setSingleShot(True)
        self.timer_congelado.timeout.connect(self.descongelar)

    # Se llama desde la ventana principal para instanciar el escenario y la partida
    def iniciar_juego(self, escenario, usuario):
        self.escenario = escenario

        # Ponderador
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

    # Se llama en el nivel inicial y cada vez que se pasa de nivel
    def iniciar_nivel(self, nivel: int) -> None:
        self.nivel = nivel
        self.pausa = False

        # Actualizar tiempo y rapidez de aliens por ponderador
        self.tiempo *= self.dificultad
        self.rapidez_aliens /= self.dificultad

        # Setear tiempo, aliens y balas del nivel
        self.timer_tiempo.setInterval(self.tiempo)
        self.cantidad_aliens = nivel * 2
        self.balas = self.cantidad_aliens * 2
        self.balas_infinitas = False

        # Resetear sets y aliens
        self.aliens = {}
        self.aliens_muertos = set()
        self.aliens_vivos = set()
        self.teclas = set()

        # Resetear tiempo y posicion mira
        self.mira.timer_disparo.setInterval(p.TIEMPO_RECARGA_NORMAL)
        self.mira.x, self.mira.y = (p.VENTANA_ANCHO / 2 - p.ANCHO_MIRA / 2,
                                    p.VENTANA_ALTO / 2 - p.ALTO_MIRA / 2)

        self.senal_iniciar_juego.emit(nivel, self.escenario, self.balas,
                                      self.tiempo, self.puntaje,
                                      (self.mira.x, self.mira.y))
        self.timer.start()
        self.timer_tiempo.start()

    # Se llama 30 veces por segundo (idealmente)
    def actualizar_juego(self):
        if not self.pausa:
            self.mira.actualizar(self.teclas)
            self.manejar_aliens()
            self.eventos()

            tiempo_restante = self.timer_tiempo.remainingTime()
            if tiempo_restante != -1:
                self.senal_actualizar_tiempo.emit(tiempo_restante)

    # Crear, eliminar y mover aliens
    def manejar_aliens(self):
        # Crear aliens mientras falten aliens por matar
        if len(self.aliens_vivos) == 0 and len(self.aliens_muertos) != self.cantidad_aliens:
            self.crear_aliens()

        # Eliminar todos los aliens en la lista
        for i in range(len(self.aliens_por_eliminar) - 1, -1, -1):
            del self.aliens[self.aliens_por_eliminar.pop(i)]

        # Mover aliens
        if not self.congelado:
            for id in self.aliens:
                self.aliens[id].mover()

    # Crear de a 2 aliens
    def crear_aliens(self):
        for i in range(2):  # Se usa 'i' para indicarle en que mitad de la pantalla aparecer
            alien = Alien(self.escenario, self.rapidez_aliens, i)
            self.aliens[alien.id] = alien
            self.aliens_vivos.add(alien.id)
            self.senal_crear_aliens.emit(
                alien.id, alien.x, alien.y, alien.width, alien.height,
                [alien.senal_posicion, alien.senal_morir, alien.senal_eliminar])
            alien.senal_eliminar.connect(self.eliminar_alien)

    # Añadir alien a lista para eliminarlos una vez llegue al final de la pantalla
    def eliminar_alien(self, id: int):
        self.aliens_por_eliminar.append(id)

        # Terminar juego cuando el ultimo alien salga de la pantalla
        if len(self.aliens_muertos) == self.cantidad_aliens and self.ultimo_disparado == id:
            self.terminar_nivel(True)

    def eventos(self):
        if random.random() < p.PROBABILIDAD_BOMBA and not self.bomba_hielo.activa:
            self.bomba_hielo.partir()

    def congelar(self):
        self.bomba_hielo.esconder()
        self.congelado = True

    def descongelar(self):
        self.congelado = False

    # Parar timer de tiempo del nivel, y dejar al perro que haga lo suyo
    def terminar_nivel(self, paso_nivel: bool):
        tiempo_restante = int(self.timer_tiempo.remainingTime() / 1000)
        self.timer_tiempo.stop()
        if paso_nivel:
            self.sonido_risa.play()
        self.senal_terminator_god.emit(paso_nivel)

        # Llamar a pasar_nivel pasado un tiempo con los argumentos respectivos
        callback = functools.partial(self.pasar_nivel, paso_nivel, tiempo_restante)
        self.timer_final.timeout.connect(callback)
        self.timer_final.start()

    # Parar timer de framerate, calcular puntaje y pasar a ventana post-nivel
    def pasar_nivel(self, paso, tiempo_restante):
        self.timer.stop()
        self.senal_esconder_ventana_juego.emit()
        if paso:
            puntos_nivel = self.calcular_puntaje_nivel(tiempo_restante)
        else:
            puntos_nivel = 0
        self.puntaje += puntos_nivel
        self.senal_terminar_nivel.emit(self.nivel, self.escenario,
                                       self.balas, tiempo_restante,
                                       self.puntaje, puntos_nivel,
                                       paso, self.usuario)

    # Calcular puntaje
    def calcular_puntaje_nivel(self, tiempo_restante) -> int:
        pts = int(self.cantidad_aliens * 100 +
                  (tiempo_restante * 30 + self.balas * 70) * self.nivel / self.dificultad)
        return pts

    # Añadir y eliminar teclas del set, además de revisar los cheatcodes
    def actualizar_teclas(self, key: int) -> None:
        if key == 80:           # tecla: p
            self.pausar_juego()

        elif key > 0:           # keyPressEvent
            self.teclas.add(key)

        else:                   # keyReleaseEvent
            self.teclas.discard(-key)

        if not self.pausa:
            if {67, 73, 65}.issubset(self.teclas):  # Cheatcode CIA
                self.terminar_nivel(True)
                self.timer_tiempo.stop()

            elif {79, 86, 78, 73}.issubset(self.teclas):  # Cheatcode OVNI
                self.balas_infinitas = True
                self.mira.balas_infinitas()
                self.senal_actualizar_balas.emit("INF")

    # Método llamado por señal de la mira cuando no esta recargando
    def disparar(self):
        if self.balas > 0:
            if not self.balas_infinitas:
                self.balas -= 1
                self.senal_actualizar_balas.emit(str(self.balas))

            self.sonido_disparo.play()

            # Ver si le dimos a algun alien
            chocados = self.chequear_colision_aliens()
            if chocados:
                self.crear_explosion(self.mira.x + self.mira.off_w,
                                     self.mira.y + self.mira.off_h)
                for id in chocados:
                    self.aliens[id].morir()
                    self.aliens_vivos.remove(id)
                    self.aliens_muertos.add(id)
                    self.ultimo_disparado = id

            if self.bomba_hielo.activa:
                if self.chequear_colision_sprite(self.bomba_hielo):
                    self.congelar()
                    self.timer_congelado.start()

            # No quedan balas
            if self.balas == 0 and len(self.aliens_muertos) != self.cantidad_aliens:
                self.pasar_nivel(False, 0)

    # Revisar colision para cada alien
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

    def chequear_colision_sprite(self, entity):
        xm = self.mira.x + self.mira.off_w
        ym = self.mira.y + self.mira.off_h

        return (xm > entity.x and xm < entity.x + entity.width and
                ym > entity.y and ym < entity.y + entity.height)

    # Crear explosion
    def crear_explosion(self, x, y):
        self.explotador.mover_explosion(x, y)
        self.explotador.start()

    # Pausar timer y reanudarlo
    def pausar_juego(self):
        self.pausa = not self.pausa
        if self.pausa:
            self.timer_tiempo.pausa()
        else:
            self.timer_tiempo.reanudar()

    # Volver al menu de inicio guardando puntaje acomulado hasta ese nivel
    def boton_volver(self):
        self.timer.stop()
        self.timer_tiempo.stop()

        # Eliminar aliens
        aliens_por_eliminar = []
        for key in self.aliens:
            aliens_por_eliminar.append(key)

        for i in aliens_por_eliminar:
            del self.aliens[i]

        guardar_puntaje(self.usuario, self.puntaje)
