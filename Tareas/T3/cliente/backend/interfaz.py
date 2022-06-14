from PyQt5.QtCore import pyqtSignal, QObject

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_espera import VentanaEspera
from frontend.ventana_juego import VentanaJuego


class Interfaz(QObject):
    #                                       (admin, users)
    senal_cargar_pantalla_espera = pyqtSignal(bool, list)
    #                                           (users)
    senal_actualizar_lista_usuarios = pyqtSignal(list)
    #                                 (users)
    senal_iniciar_partida = pyqtSignal(list)
    #                              (en_turno, usuarios)
    senal_actualizar_juego = pyqtSignal(bool, list)

    def __init__(self, parent):
        super().__init__()

        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()

        #  CONEXIONES
        self.ventana_inicio.senal_enviar_usuario.connect(parent.enviar_mensaje)
        self.ventana_espera.senal_iniciar_juego.connect(parent.enviar_mensaje)
        self.ventana_juego.senal_tirar_dado.connect(parent.enviar_mensaje)

        self.senal_cargar_pantalla_espera.connect(self.ventana_espera.cargar_pantalla)
        self.senal_actualizar_lista_usuarios.connect(self.ventana_espera.cargar_usuarios)
        self.senal_iniciar_partida.connect(self.ventana_juego.init_gui)
        self.senal_actualizar_juego.connect(self.ventana_juego.actualizar_juego)

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
        elif comando == "actualizar_lista_usuarios":
            self.senal_actualizar_lista_usuarios.emit(mensaje["usuarios"])
        elif comando == "repuesta_iniciar_partida":
            if mensaje["estado"] == "aceptado":
                self.ventana_espera.esconder()
                self.senal_iniciar_partida.emit(mensaje["usuarios"])
            else:
                print("ERROR FATAL")
        elif comando == "actualizar_juego":
            self.senal_actualizar_juego.emit(mensaje["en_turno"], [])
