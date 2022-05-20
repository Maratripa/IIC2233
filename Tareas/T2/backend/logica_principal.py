from PyQt5.QtCore import QObject, pyqtSignal


class LogicaPrincipal(QObject):
    #                                    (valido, errores)
    senal_respuesta_validacion = pyqtSignal(bool, list)

    def __init__(self) -> None:
        super().__init__()

    def comprobar_usuario(self, usuario: str) -> None:
        errores = []
        valido = True

        if not usuario:
            errores.append("null")
            valido = False
        elif not usuario.isalnum():
            errores.append("alnum")
            valido = False

        self.senal_respuesta_validacion.emit(valido, errores)
