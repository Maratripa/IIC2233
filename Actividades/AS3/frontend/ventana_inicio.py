import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QPushButton)
import parametros as p


class VentanaInicio(QWidget):

    senal_enviar_login = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()

        # Geometría
        self.setGeometry(600, 200, 500, 500)
        self.setWindowTitle('Ventana de Inicio')
        self.setStyleSheet("background-color: lightblue;")
        self.crear_elementos()

    def crear_elementos(self):
        # CCOMPLETAR
        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(p.RUTA_LOGO))

        self.label1 = QLabel("Ingresa tu nombre de usuario:", self)
        self.usuario = QLineEdit("", self)

        self.label2 = QLabel("Ingresa la contraseña:", self)
        self.contrasena = QLineEdit("", self)

        self.submit = QPushButton("Empezar juego!", self)
        self.submit.clicked.connect(self.enviar_login)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label1)
        hbox1.addWidget(self.usuario)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.label2)
        hbox2.addWidget(self.contrasena)
        hbox2.addStretch(1)

        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.submit)
        hbox3.addStretch(1)

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.logo)
        vbox1.addLayout(hbox1)
        vbox1.addLayout(hbox2)
        vbox1.addLayout(hbox3)

        self.setLayout(vbox1)

    def enviar_login(self):
        # COMPLETAR
        usuario = self.usuario.text()
        cont = self.contrasena.text()

        self.senal_enviar_login.emit((usuario, cont))

    def recibir_validacion(self, valid: bool, errores: list):
        # COMPLETAR
        if valid:
            self.hide()
        else:
            if "Usuario" in errores:
                self.usuario.setText("")
                self.contrasena.setText("")
                self.usuario.setPlaceholderText("Usuario inválido")
            if "Contraseña" in errores:
                self.usuario.setText("")
                self.contrasena.setText("")
                self.contrasena.setPlaceholderText("Contraseña inválida")


if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.crear_elementos()
    ventana.show()
    sys.exit(app.exec_())
