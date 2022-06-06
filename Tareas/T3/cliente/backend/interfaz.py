from PyQt5.QtCore import pyqtSignal, QObject

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_espera import VentanaEspera


class Interfaz(QObject):
    #                                       (admin, users)
    senal_cargar_pantalla_espera = pyqtSignal(bool, list)

    def __init__(self, parent):
        super().__init__()

        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()

        #  CONEXIONES
        self.ventana_inicio.senal_enviar_usuario.connect(parent.enviar_mensaje)

        self.senal_cargar_pantalla_espera.connect(self.ventana_espera.cargar_pantalla)

    def mostrar_ventana_inicio(self):
        self.ventana_inicio.mostrar()

    def procesar_mensaje(self, mensaje: dict) -> dict:
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "respuesta_validacion_login":
            if mensaje["estado"] == "aceptado":
                self.ventana_inicio.esconder()
                self.senal_cargar_pantalla_espera.emit(mensaje["admin"], mensaje["usuarios"])
            else:
                self.ventana_inicio.error_usuario(mensaje["error"])
