from PyQt5.QtCore import QObject, pyqtSignal

import parametros as p


class LogicaInicio(QObject):

    senal_respuesta_validacion = pyqtSignal(bool, list)
    senal_abrir_juego = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def comprobar_usuario(self, tupla_respuesta: tuple):
        # COMPLETAR
        usuario, contrasena = tupla_respuesta
        errores = []
        valido = True

        if not usuario.isalnum() or len(usuario) > p.MAX_CARACTERES:
            errores.append("Usuario")
            valido = False
        if contrasena != p.PASSWORD:
            errores.append("Contraseña")
            valido = False

        self.senal_respuesta_validacion.emit(valido, errores)

        if valido:
            self.senal_abrir_juego.emit(usuario)
