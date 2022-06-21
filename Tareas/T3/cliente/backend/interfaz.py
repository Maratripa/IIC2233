from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QWidget, QLabel)

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_espera import VentanaEspera
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_final import VentanaFinal


class Interfaz(QObject):
    #                                       (users, admin)
    senal_cargar_pantalla_espera = pyqtSignal(list, bool)
    #                                           (users)
    senal_actualizar_lista_usuarios = pyqtSignal(list)
    #
    senal_hacer_admin = pyqtSignal()
    #                                 (users)
    senal_iniciar_partida = pyqtSignal(list)
    #                                  (mensaje)
    senal_actualizar_juego = pyqtSignal(dict)
    #                                   (ganador, users)
    senal_cargar_pantalla_final = pyqtSignal(str, list)
    #                                      (info)
    senal_actualizar_jugadores = pyqtSignal(dict)

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.ventana_inicio = VentanaInicio()
        self.ventana_espera = VentanaEspera()
        self.ventana_juego = VentanaJuego()
        self.ventana_final = VentanaFinal()

        #  CONEXIONES
        self.ventana_inicio.senal_enviar_usuario.connect(parent.enviar_mensaje)
        self.ventana_espera.senal_iniciar_juego.connect(parent.enviar_mensaje)
        self.ventana_juego.senal_tirar_dado.connect(parent.enviar_mensaje)
        self.ventana_final.senal_volver_inicio.connect(self.volver_inicio)

        self.senal_cargar_pantalla_espera.connect(self.ventana_espera.cargar_usuarios)
        self.senal_actualizar_lista_usuarios.connect(self.ventana_espera.cargar_usuarios)
        self.senal_hacer_admin.connect(self.ventana_espera.hacer_admin)
        self.senal_iniciar_partida.connect(self.ventana_juego.cargar_usuarios)
        self.senal_actualizar_juego.connect(self.ventana_juego.actualizar_juego)
        self.senal_actualizar_jugadores.connect(self.ventana_juego.actualizar_jugadores)
        self.senal_cargar_pantalla_final.connect(self.ventana_final.cargar_usuarios)

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
                self.senal_cargar_pantalla_espera.emit(mensaje["usuarios"], mensaje["admin"])
                self.ventana_espera.mostrar()
            else:
                self.ventana_inicio.error_usuario(mensaje["error"])
        elif comando == "actualizar_lista_usuarios":
            self.senal_actualizar_lista_usuarios.emit(mensaje["usuarios"])
        elif comando == "soy_admin":
            self.senal_hacer_admin.emit()
        elif comando == "repuesta_iniciar_partida":
            if mensaje["estado"] == "aceptado":
                self.ventana_espera.esconder()
                self.senal_iniciar_partida.emit(mensaje["usuarios"])
            else:
                print("ERROR FATAL")
        elif comando == "actualizar_juego":
            self.senal_actualizar_juego.emit(mensaje)
        elif comando == "terminar_juego":
            self.ventana_juego.esconder()
            self.senal_cargar_pantalla_final.emit(mensaje['ganador'], mensaje['usuarios'])
        elif comando == "actualizar_lista_jugadores":
            self.senal_actualizar_jugadores.emit(mensaje)
    
    def volver_inicio(self):
        self.ventana_final.esconder()
        self.ventana_inicio.mostrar()

        mensaje = {"comando": "volver_inicio"}
        self.parent.enviar_mensaje(mensaje)
    
    def mostrar_popup(self, mensaje: str):
        self.popup = PopUp(mensaje)
        self.popup.senal_cerrar.connect(self.cerrar)
        self.popup.show()
    
    def cerrar(self):
        self.parent.socket_cliente.close()
        self.ventana_inicio.close()
        self.ventana_espera.close()
        self.ventana_juego.close()
        self.ventana_final.close()
class PopUp(QWidget):

    senal_cerrar = pyqtSignal()

    def __init__(self, mensaje):
        super().__init__()

        mensaje = QLabel(mensaje, self)

        self.setWindowTitle("Error")
        self.setGeometry(400, 200, 200, 100)
    
    def closeEvent(self, event):
        self.senal_cerrar.emit()
        event.accept()