from PyQt5.QtCore import pyqtSignal, QObject

from frontend.ventana_inicio import VentanaInicio


class Interfaz(QObject):
    def __init__(self, parent):
        super().__init__()
        self.ventana_inicio = VentanaInicio()

    def mostrar_ventana_inicio(self):
        self.ventana_inicio.mostrar()
