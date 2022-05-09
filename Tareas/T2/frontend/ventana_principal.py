import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QRadioButton, QLineEdit)

import utils


class VentanaPrincipal(QWidget):

    senal_enviar_login = pyqtSignal(str)
    senal_abrir_juego = pyqtSignal(int, str)

    def __init__(self) -> None:
        super().__init__()

        # Geometria
        self.setGeometry(600, 200, 600, 400)
        self.setWindowTitle("A cazar aliens!")
        self.crear_elementos()

    def crear_elementos(self) -> None:
        # Etiquetas
        self.titulo = QLabel("Elige el ambiente de caza espacial", self)

        # Escenarios
        self.escenario_1 = QLabel(self)
        pixmap_e1 = QPixmap("frontend/assets/Sprites/Fondos/Luna.png")
        self.escenario_1.setPixmap(pixmap_e1.scaled(160, 100))

        self.escenario_2 = QLabel(self)
        pixmap_e2 = QPixmap("frontend/assets/Sprites/Fondos/Jupiter.png")
        self.escenario_2.setPixmap(pixmap_e2.scaled(160, 100))

        self.escenario_3 = QLabel(self)
        pixmap_e3 = QPixmap("frontend/assets/Sprites/Fondos/Galaxia.png")
        self.escenario_3.setPixmap(pixmap_e3.scaled(160, 100))

        # Iconos
        self.icono_1 = QLabel(self)
        pixmap_i1 = QPixmap("frontend/assets/Sprites/Aliens/Alien1.png")
        self.icono_1.setPixmap(pixmap_i1.scaled(30, 30, 1, 1))

        self.icono_2 = QLabel(self)
        pixmap_i2 = QPixmap("frontend/assets/Sprites/Aliens/Alien2.png")
        self.icono_2.setPixmap(pixmap_i2.scaled(30, 30, 1, 1))

        self.icono_3 = QLabel(self)
        pixmap_i3 = QPixmap("frontend/assets/Sprites/Aliens/Alien3.png")
        self.icono_3.setPixmap(pixmap_i3.scaled(30, 30, 1, 1))

        # Botones
        self.boton_1 = QRadioButton("Tutorial lunar", self)
        self.boton_1.click()  # Opcion por default
        self.boton_2 = QRadioButton("Entrenamiento en Júpiter", self)
        self.boton_3 = QRadioButton("Invasión intergaláctica", self)

        self.boton_submit = QPushButton("Cazar aquí", self)
        self.boton_submit.clicked.connect(self.enviar_login)

        # Input usuario
        self.label_1 = QLabel("Nombre de astronauta", self)
        self.input_1 = QLineEdit(self)

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
        vbox5.addStretch(1)
        vbox5.addLayout(hbox6)
        vbox5.addStretch(1)

        self.setLayout(vbox5)

    def enviar_login(self) -> None:
        self.senal_enviar_login.emit(self.input_1.text())

    def recibir_validacion(self, valido: bool, errores: list) -> None:
        if valido:
            self.hide()

            nivel = 0
            if self.boton_1.isChecked():
                nivel = 1
            elif self.boton_2.isChecked():
                nivel = 2
            elif self.boton_3.isChecked():
                nivel = 3

            self.senal_abrir_juego.emit(nivel, self.input_1.text())
        else:
            if "alnum" in errores:
                self.input_1.setText("")
                self.input_1.setPlaceholderText("Use alpha-numeric characters for username")
            if "null" in errores:
                self.input_1.setPlaceholderText("Enter a username")


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPrincipal()
    sys.exit(app.exec_())
