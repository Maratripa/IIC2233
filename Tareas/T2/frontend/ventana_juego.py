import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QProgressBar)


class VentanaJuego(QWidget):

    senal_boton_salir = pyqtSignal()
    senal_boton_pausa = pyqtSignal()
    senal_actualizar_teclas = pyqtSignal(set)

    def __init__(self):
        super().__init__()

        # Teclas apretadas
        self.teclas = set()

        # Geometria
        self.setGeometry(200, 200, 960, 700)
        self.setWindowTitle("A cazar aliens!")
        self.setStyleSheet(
            "font-size: 16px;",
        )
        self.setFixedSize(960, 700)

        # Fondo
        self.bg = QLabel(self)
        pixmap_bg = QPixmap()
        self.bg.setPixmap(pixmap_bg.scaled(960, 600, 2, 1))
        self.bg.setGeometry(0, 0, 960, 600)

        # Alien pixmaps
        self.pixmap_alien = QPixmap()
        self.pixmap_alien_muerto = QPixmap()

        # Barra inferior
        # VBox tiempo
        self.label_tiempo = QLabel("Tiempo", self)
        self.barra_timepo = QProgressBar(self)
        self.barra_timepo.setTextVisible(False)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.label_tiempo)
        vbox1.addWidget(self.barra_timepo)

        # VBox balas
        self.label_balas = QLabel("Balas", self)

        self.icono_bala = QLabel(self)
        self.pixmap_bala = QPixmap(
            "frontend/assets/Sprites/Elementos juego/Bala.png")
        self.icono_bala.setPixmap(self.pixmap_bala.scaled(10, 20))

        self.cuenta_balas = QLabel(f"X 0", self)

        hbox0_1 = QHBoxLayout()
        hbox0_1.addWidget(self.icono_bala)
        hbox0_1.addWidget(self.cuenta_balas)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.label_balas)
        vbox2.addLayout(hbox0_1)

        # VBox puntaje
        self.label_puntaje = QLabel("Puntaje", self)
        self.cuenta_puntaje = QLabel("0 ptos", self)

        vbox3 = QVBoxLayout()
        vbox3.addWidget(self.label_puntaje)
        vbox3.addWidget(self.cuenta_puntaje)

        # Vbox nivel
        self.label_nivel = QLabel("Nivel", self)
        self.cuenta_nivel = QLabel(f"0", self)

        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.label_nivel)
        vbox4.addWidget(self.cuenta_nivel)

        # VBox botones
        self.boton_pausa = QPushButton("Pausa", self)
        self.boton_pausa.clicked.connect(self.pausar_juego)
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.salir_juego)

        vbox5 = QVBoxLayout()
        vbox5.addWidget(self.boton_pausa)
        vbox5.addWidget(self.boton_salir)

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
        label_vacio = QLabel(self)
        label_vacio.setGeometry(0, 0, 960, 600)

        vbox6 = QVBoxLayout()
        vbox6.addWidget(label_vacio)
        vbox6.addLayout(hbox2)

        vbox6.setContentsMargins(11, 11, 11, 20)

        # Setear Layout
        self.setLayout(vbox6)

    def iniciar_juego(self):
        pass

    def keyPressEvent(self, event):
        self.teclas.add(event.key())
        self.senal_actualizar_teclas.emit(self.teclas)

    def keyReleaseEvent(self, event):
        self.teclas.remove(event.key())
        self.senal_actualizar_teclas.emit(self.teclas)

    def salir_juego(self):
        self.senal_boton_salir.emit()

    def pausar_juego(self):
        self.senal_boton_pausa.emit()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaJuego("assets/Sprites/Fondos/Galaxia.png", 1, 60, 100)
    sys.exit(app.exec_())
