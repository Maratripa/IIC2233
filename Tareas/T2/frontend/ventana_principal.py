from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QRadioButton, QLineEdit)
import parametros as p
import utils


class VentanaPrincipal(QWidget):

    senal_enviar_login = pyqtSignal(str)
    #
    senal_abrir_juego = pyqtSignal(int, str)

    def __init__(self) -> None:
        super().__init__()

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO, p.VENTANA_ALTO)
        self.setWindowTitle("A cazar aliens!")

        # Etiquetas
        self.titulo = QLabel("Elige el ambiente de caza espacial", self)
        self.titulo.setObjectName("titulo")

        # Escenarios
        self.escenario_1 = QLabel(self)
        pixmap_e1 = QPixmap(path.join(*p.RUTA_FONDO, "Luna.png"))
        self.escenario_1.setPixmap(pixmap_e1.scaled(p.ANCHO_PREVIEW, p.ALTO_PREVIEW))

        self.escenario_2 = QLabel(self)
        pixmap_e2 = QPixmap(path.join(*p.RUTA_FONDO, "Jupiter.png"))
        self.escenario_2.setPixmap(pixmap_e2.scaled(p.ANCHO_PREVIEW, p.ALTO_PREVIEW))

        self.escenario_3 = QLabel(self)
        pixmap_e3 = QPixmap(path.join(*p.RUTA_FONDO, "Galaxia.png"))
        self.escenario_3.setPixmap(pixmap_e3.scaled(p.ANCHO_PREVIEW, p.ALTO_PREVIEW))

        # Iconos
        self.icono_1 = QLabel(self)
        pixmap_i1 = QPixmap(path.join(*p.RUTA_ALIEN, "Alien1.png"))
        self.icono_1.setPixmap(pixmap_i1.scaled(p.ANCHO_ICONOS[0], p.ALTO_ICONOS[0], 1, 1))

        self.icono_2 = QLabel(self)
        pixmap_i2 = QPixmap(path.join(*p.RUTA_ALIEN, "Alien2.png"))
        self.icono_2.setPixmap(pixmap_i2.scaled(p.ANCHO_ICONOS[1], p.ALTO_ICONOS[1], 1, 1))

        self.icono_3 = QLabel(self)
        pixmap_i3 = QPixmap(path.join(*p.RUTA_ALIEN, "Alien3.png"))
        self.icono_3.setPixmap(pixmap_i3.scaled(p.ANCHO_ICONOS[2], p.ALTO_ICONOS[2], 1, 1))

        # Botones
        self.boton_1 = QRadioButton("Tutorial lunar", self)
        self.boton_2 = QRadioButton("Entrenamiento en Júpiter", self)
        self.boton_3 = QRadioButton("Invasión intergaláctica", self)
        self.boton_1.click()  # Opcion por default

        self.boton_submit = QPushButton("Cazar aquí", self)
        self.boton_submit.clicked.connect(self.enviar_login)

        # Input usuario
        self.label_1 = QLabel("Nombre de astronauta:", self)
        self.label_1.sizeHint()
        self.input_1 = QLineEdit(self)
        self.label_error = QLabel(self)
        self.label_error.setObjectName("error")

        # HLayout 1
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.titulo)
        hbox1.addStretch(1)

        # VLayout 1
        vbox1 = QVBoxLayout()
        vbox1.addLayout(utils.encapsular_h(self.escenario_1))
        vbox1.addLayout(utils.encapsular_h(self.icono_1))
        vbox1.addLayout(utils.encapsular_h(self.boton_1))

        # VLayout 2
        vbox2 = QVBoxLayout()
        vbox2.addLayout(utils.encapsular_h(self.escenario_2))
        vbox2.addLayout(utils.encapsular_h(self.icono_2))
        vbox2.addLayout(utils.encapsular_h(self.boton_2))

        # VLayout 3
        vbox3 = QVBoxLayout()
        vbox3.addLayout(utils.encapsular_h(self.escenario_3))
        vbox3.addLayout(utils.encapsular_h(self.icono_3))
        vbox3.addLayout(utils.encapsular_h(self.boton_3))

        # HLayout 2
        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addLayout(vbox1)
        hbox2.addStretch(1)
        hbox2.addLayout(vbox2)
        hbox2.addStretch(1)
        hbox2.addLayout(vbox3)
        hbox2.addStretch(1)

        # Hlayout 5
        # VLayout 4
        vbox4 = QVBoxLayout()
        vbox4.addWidget(self.label_1)
        vbox4.addWidget(self.input_1)
        vbox4.addWidget(self.label_error)

        hbox5 = QHBoxLayout()
        hbox5.addStretch(1)
        hbox5.addLayout(vbox4)
        hbox5.addStretch(7)

        # HLayout 6
        hbox6 = QHBoxLayout()
        hbox6.addStretch(1)
        hbox6.addWidget(self.boton_submit)
        hbox6.addStretch(1)

        # VLayout 5 (final)
        vbox5 = QVBoxLayout()
        vbox5.addStretch(1)
        vbox5.addLayout(hbox1)
        vbox5.addStretch(1)
        vbox5.addLayout(hbox2)
        vbox5.addStretch(2)
        vbox5.addLayout(hbox5)
        vbox5.addLayout(hbox6)
        vbox5.addStretch(1)

        self.setLayout(vbox5)

    # Enviar usuario para ser validado
    def enviar_login(self) -> None:
        self.senal_enviar_login.emit(self.input_1.text())

    # Pasar al juego si el usuario es valido, mostrar error en caso contrario
    def recibir_validacion(self, valido: bool, errores: list) -> None:
        if valido:
            self.hide()

            if self.boton_1.isChecked():
                escenario = 1
            elif self.boton_2.isChecked():
                escenario = 2
            elif self.boton_3.isChecked():
                escenario = 3

            self.senal_abrir_juego.emit(escenario, self.input_1.text())
        else:
            if "alnum" in errores:
                self.input_1.setText("")
                self.label_error.setText(" Usa carácteres alfanuméricos")
            if "null" in errores:
                self.label_error.setText(" Ingresa un usuario")
