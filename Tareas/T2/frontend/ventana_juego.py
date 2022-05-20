from os import path

from PyQt5.QtCore import pyqtSignal, QTimer, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout,
                             QHBoxLayout, QPushButton,
                             QProgressBar)
import parametros as p


class VentanaJuego(QWidget):

    senal_boton_volver = pyqtSignal()
    senal_boton_pausa = pyqtSignal()
    #                                   (key)
    senal_actualizar_teclas = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFocus()

        # Timer de espera para volver la mira normal
        self.timer_mira_roja = QTimer(self)
        self.timer_mira_roja.setInterval(1000)
        self.timer_mira_roja.setSingleShot(True)
        self.timer_mira_roja.timeout.connect(self.mira_normal)

        # Barra inferior
        self.barra_inferior = QLabel(self)
        self.barra_inferior.setGeometry(0, 600, p.VENTANA_ANCHO, 100)

        # Diccionario labels aliens
        self.aliens = {}

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO, p.VENTANA_ALTO + 100)
        self.setWindowTitle("A cazar aliens!")
        self.setFixedSize(p.VENTANA_ANCHO, p.VENTANA_ALTO + 100)

        # Mira
        self.label_mira = QLabel(self)
        self.label_mira.setObjectName("sprite")
        self.pixmap_mira = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparador_negro.png"))
        self.pixmap_mira_roja = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparador_rojo.png"))
        self.label_mira.setPixmap(self.pixmap_mira)
        self.label_mira.setGeometry(0, 0, p.ANCHO_MIRA, p.ALTO_MIRA)
        self.label_mira.setScaledContents(True)
        self.label_mira.stackUnder(self.barra_inferior)

        # Explosion
        self.label_explosion = QLabel(self)
        self.label_explosion.setObjectName("sprite")
        self.label_explosion.stackUnder(self.label_mira)
        self.label_explosion.setScaledContents(True)
        self.label_explosion.hide()
        # Posicion explosion
        self.label_explosion.posicion = (0, 0)
        # Pixmaps explosiones
        self.pixmap_explosiones = [
            QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparo_f1.png")),
            QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparo_f2.png")),
            QPixmap(path.join(*p.RUTA_ELEMENTOS, "Disparo_f3.png"))
        ]

        # Barra inferior
        # VBox tiempo
        self.label_tiempo = QLabel("Tiempo", self)
        self.label_tiempo.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.barra_tiempo = QProgressBar(self)
        self.barra_tiempo.setTextVisible(False)

        vboxtiempo = QVBoxLayout()
        vboxtiempo.addStretch(1)
        vboxtiempo.addWidget(self.barra_tiempo)
        vboxtiempo.addStretch(1)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label_tiempo)
        vbox1.addLayout(vboxtiempo)

        # VBox balas
        self.label_balas = QLabel("Balas", self)
        self.label_balas.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.icono_bala = QLabel(self)
        self.pixmap_bala = QPixmap(path.join(*p.RUTA_ELEMENTOS, "Bala.png"))
        self.icono_bala.setPixmap(self.pixmap_bala.scaled(20, 40, 1, 1))

        self.cuenta_balas = QLabel(f"X 0", self)

        hbox0_1 = QHBoxLayout()
        hbox0_1.addWidget(self.icono_bala)
        hbox0_1.addWidget(self.cuenta_balas)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label_balas)
        vbox2.addLayout(hbox0_1)

        # VBox puntaje
        self.label_puntaje = QLabel("Puntaje", self)
        self.label_puntaje.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cuenta_puntaje = QLabel("0 ptos", self)
        self.cuenta_puntaje.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label_puntaje)
        vbox3.addWidget(self.cuenta_puntaje)

        # Vbox nivel
        self.label_nivel = QLabel("Nivel", self)
        self.label_nivel.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.cuenta_nivel = QLabel(f"0", self)
        self.cuenta_nivel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.label_nivel)
        vbox4.addWidget(self.cuenta_nivel)

        # VBox botones
        self.boton_pausa = QPushButton("Pausa", self)
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.boton_pausa.setFocusPolicy(4)

        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.clicked.connect(self.volver)
        self.boton_volver.setFocusPolicy(4)

        vbox5 = QVBoxLayout()
        vbox5.addWidget(self.boton_pausa)
        vbox5.addWidget(self.boton_volver)

        # HBox barra
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox1)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox2)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox3)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox4)
        hbox2.addStretch(2)
        hbox2.addLayout(vbox5)
        hbox2.addStretch(1)

        # VBox global
        # Label para poner barra abajo
        self.label_vacio = QLabel(self)
        self.label_vacio.stackUnder(self.label_explosion)
        self.label_vacio.setObjectName("vacio")
        self.label_vacio.setFixedSize(p.VENTANA_ANCHO, p.VENTANA_ALTO)

        vbox6 = QVBoxLayout()
        vbox6.addWidget(self.label_vacio)
        vbox6.addLayout(hbox2)

        # Setear Layout
        self.setLayout(vbox6)

        # Terminator god
        self.god = QLabel(self)
        self.god.setObjectName("sprite")
        self.god.stackUnder(self.label_mira)
        #                                  ancho grande para escalar segun altura
        self.god.setGeometry(0, p.GOD_POS_Y, p.VENTANA_ANCHO, p.GOD_HEIGHT)
        self.pixmap_god_1 = QPixmap(path.join(*p.RUTA_GOD, "Dog1.png")).scaled(
            p.VENTANA_ANCHO, p.GOD_HEIGHT, 1, 1)
        self.god.setPixmap(self.pixmap_god_1)

        # Pixmaps de perro y aliens
        self.god_aliens = [
            QPixmap(path.join(*p.RUTA_GOD, "Perro_y_alien1.png")),
            QPixmap(path.join(*p.RUTA_GOD, "Perro_y_alien2.png")),
            QPixmap(path.join(*p.RUTA_GOD, "Perro_y_alien3.png"))
        ]

    # Esta funcion inicia todos los niveles y resetea labels a los valores iniciales
    def iniciar_nivel(self, nivel, escenario, balas, tiempo, pos_mira: tuple):
        self.nivel = nivel
        self.escenario = escenario

        # Resetear aliens
        self.aliens = {}

        self.cuenta_nivel.setText(f"{nivel}")
        self.cuenta_balas.setText(f"X {balas}")

        # Mapeo del tiempo a porcentaje
        self.barra_tiempo.setRange(0, int(tiempo / 1000))
        self.barra_tiempo.setValue(int(tiempo / 1000))

        if escenario == 1:
            pixmap_bg = QPixmap(path.join(*p.RUTA_FONDO, "Luna.png"))
        elif escenario == 2:
            pixmap_bg = QPixmap(path.join(*p.RUTA_FONDO, "Jupiter.png"))
        elif escenario == 3:
            pixmap_bg = QPixmap(path.join(*p.RUTA_FONDO, "Galaxia.png"))

        # Fondo
        self.bg = QLabel(self)
        self.bg.setPixmap(pixmap_bg.scaled(p.VENTANA_ANCHO, p.VENTANA_POS_Y, 2, 1))
        self.bg.setGeometry(0, 0, 960, 600)
        self.bg.setScaledContents(True)
        self.bg.stackUnder(self.label_vacio)

        # Alien pixmaps
        self.pixmap_alien = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{escenario}.png"))
        self.pixmap_alien_muerto = QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{escenario}_dead.png"))

        # Mira pixmap
        self.mira_normal()
        self.label_mira.move(*pos_mira)

        # GOD Pixmap
        self.god.setPixmap(self.pixmap_god_1)
        self.show()

    # Enviar numero de tecla apretada para añadirla al set
    def keyPressEvent(self, event):
        self.senal_actualizar_teclas.emit(event.key())

    # Enviar negativo del numero de la tecla para sacarla del set
    def keyReleaseEvent(self, event):
        self.senal_actualizar_teclas.emit(-event.key())

    # Crear label alien
    def agregar_label_alien(self, id, x, y, ancho, alto, senales):
        label = QLabel(self)
        label.setObjectName("sprite")
        label.setPixmap(self.pixmap_alien)
        label.setGeometry(x, y, ancho, alto)
        label.setScaledContents(True)
        label.stackUnder(self.label_explosion)
        self.aliens[id] = label
        label.show()

        # Conectar señales del alien
        senales[0].connect(self.mover_alien)
        senales[1].connect(self.matar_alien)
        senales[2].connect(self.eliminar_alien)

    # Mover alien
    def mover_alien(self, id: int, pos: tuple):
        self.aliens[id].move(*pos)

    # Cambiar pixmap alien
    def matar_alien(self, id: int):
        self.aliens[id].setPixmap(self.pixmap_alien_muerto)

    # Elimiar alien del diccionario
    def eliminar_alien(self, id: int):
        self.aliens[id].hide()
        del self.aliens[id]

    # Mover mira
    def mover_mira(self, pos: tuple):
        self.label_mira.move(*pos)

    # Cambiar mira a roja
    def cambiar_mira(self):
        self.label_mira.setPixmap(self.pixmap_mira_roja)
        self.timer_mira_roja.start()

    # Cambiar mira a normal

    def mira_normal(self):
        self.label_mira.setPixmap(self.pixmap_mira)

    # Cambiar lugar de explosión
    def mover_explosion(self, x, y):
        self.label_explosion.posicion = (x, y)

    # Visibilizar explosión y cambiar los pixmap
    def explosion(self, fase):
        self.label_explosion.setPixmap(self.pixmap_explosiones[fase])

        x, y = self.label_explosion.posicion
        self.label_explosion.setGeometry(x - p.ANCHO_EXPLOSION[fase] / 2,
                                         y - p.ALTO_EXPLOSION[fase] / 2,
                                         p.ANCHO_EXPLOSION[fase], p.ALTO_EXPLOSION[fase])
        if fase == 0:
            self.label_explosion.show()
        elif fase == -1:
            self.label_explosion.hide()

    # Actualizar balas
    def actualizar_balas(self, balas):
        self.cuenta_balas.setText(f"X {balas}")

    # Actualizar barra tiempo
    def actualizar_tiempo(self, tiempo):
        self.barra_tiempo.setValue(int(tiempo / 1000))
        self.barra_tiempo.repaint()

    # Cambiar pixmap de perro
    def fin_nivel(self, paso):
        if paso:
            self.god.setPixmap(self.god_aliens[self.escenario - 1].scaled(
                p.VENTANA_ANCHO, p.GOD_HEIGHT, 1, 1))
            self.repaint()

    # Boton volver al menu de inicio
    def volver(self):
        # Esconder todos los aliens presentes
        for key in self.aliens:
            self.aliens[key].hide()

        self.senal_boton_volver.emit()
        self.hide()

    # Boton pausa
    def pausar_juego(self):
        self.senal_boton_pausa.emit()
