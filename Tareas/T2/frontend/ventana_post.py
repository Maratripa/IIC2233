import sys
from os import path
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QFormLayout, QLabel,
                             QVBoxLayout, QHBoxLayout, QPushButton,
                             QApplication)
import parametros as p
import utils


class VentanaPost(QWidget):
    #                                 (nivel)
    senal_siguiente_nivel = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        # Geometria
        self.setGeometry(p.VENTANA_POS_X, p.VENTANA_POS_Y, p.VENTANA_ANCHO / 2, p.VENTANA_ALTO)
        self.setWindowTitle("A cazar aliens!")

        # Titulo
        self.label_titulo = QLabel("RESUMEN DEL NIVEL ", self)
        self.label_titulo.setObjectName("titulo")
        self.icono_titulo = QLabel(self)

        self.pixmaps = []
        for i in range(3):
            self.pixmaps.append(QPixmap(path.join(*p.RUTA_ALIEN, f"Alien{i + 1}_dead.png")))

        # Nivel
        self.label_nivel = QLabel("Nivel actual", self)
        self.nivel = QLabel("0", self)

        # Balas
        self.label_balas = QLabel("Balas restantes", self)
        self.balas = QLabel("0", self)

        # Tiempo
        self.label_tiempo = QLabel("Tiempo restante", self)
        self.tiempo = QLabel("0 seg", self)

        # Puntaje
        self.label_puntaje = QLabel("Puntaje total", self)
        self.puntaje = QLabel("0 ptos", self)

        # Puntaje nivel
        self.label_puntaje_nivel = QLabel("Puntaje obtenido en nivel", self)
        self.puntaje_nivel = QLabel("0 ptos", self)

        # Mensaje nivel
        self.label_mensaje = QLabel("", self)

        # Botones
        self.boton_siguiente = QPushButton("Siguiente nivel", self)
        self.boton_siguiente.clicked.connect(self.siguiente_nivel)
        self.boton_salir = QPushButton("Salir", self)
        self.boton_salir.clicked.connect(self.salir)

        # HBox 1
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.label_titulo)
        hbox1.addWidget(self.icono_titulo)
        hbox1.addStretch(1)

        # FormLayout 1
        formlayout1 = QFormLayout()
        formlayout1.addRow(self.label_nivel, self.nivel)
        formlayout1.addRow(self.label_balas, self.balas)
        formlayout1.addRow(self.label_tiempo, self.tiempo)
        formlayout1.addRow(self.label_puntaje, self.puntaje)
        formlayout1.addRow(self.label_puntaje_nivel, self.puntaje_nivel)

        # HBox 2
        hbox2 = utils.encapsular_h(self.label_mensaje)

        # HBox 3
        hbox3 = QHBoxLayout()
        hbox3.addStretch(1)
        hbox3.addWidget(self.boton_siguiente)
        hbox3.addStretch(1)
        hbox3.addWidget(self.boton_salir)
        hbox3.addStretch(1)

        # VBox 1
        vbox1 = QVBoxLayout()
        vbox1.addStretch(1)
        vbox1.addLayout(hbox1)
        vbox1.addStretch(1)
        vbox1.addLayout(utils.encapsular_h(formlayout1))
        vbox1.addStretch(1)
        vbox1.addLayout(hbox2)
        vbox1.addStretch(1)
        vbox1.addLayout(hbox3)
        vbox1.addStretch(1)

        self.setLayout(vbox1)

    def mostrar(self, nivel, escenario, balas, tiempo, puntaje, puntaje_nivel, siguiente):
        self.escenario = escenario
        self.icono_titulo.setPixmap(
            self.pixmaps[escenario - 1].scaled(
                p.ANCHO_ICONOS[escenario - 1], p.ALTO_ICONOS[escenario - 1]))
        self.nivel.setText(f"{nivel}")
        self.balas.setText(f"{balas}")
        self.tiempo.setText(f"{tiempo} seg")
        self.puntaje.setText(f"{puntaje} ptos")
        self.puntaje_nivel.setText(f"{puntaje_nivel} ptos")

        if siguiente:
            self.label_mensaje.setText("¡Puedes dominar el siguiente nivel!")
            self.label_mensaje.setStyleSheet("""
                background-color: #ABE9B3;
                color: #1A1826;
                padding: 5px 5px;
            """)
            self.boton_siguiente.setEnabled(True)
        else:
            self.label_mensaje.setText("¡Perdiste! No puedes seguir jugando :(")
            self.label_mensaje.setStyleSheet("""
                background-color: #F28FAD;
                color: white;
                padding: 5px 5px;
            """)
            self.boton_siguiente.setEnabled(False)

        self.show()

    def siguiente_nivel(self):
        self.senal_siguiente_nivel.emit(int(self.nivel.text()) + 1)
        self.hide()

    def salir(self):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    ventana = VentanaPost()
    ventana.show()
    sys.exit(app.exec_())
