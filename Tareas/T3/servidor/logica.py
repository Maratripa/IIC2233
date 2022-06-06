import random
from utils import data_json


class Logica:
    def __init__(self, parent):
        self.parent = parent

        self.usuarios = []

        self.colores = ("rojo", "amarillo", "azul", "verde")
        self.colores_idx = [0, 1, 2, 3]

    def procesar_mensaje(self, mensaje: dict, socket_cliente, id_cliente: int) -> None:
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "validar_login":
            respuesta, socket_resp = self.validar_login(
                mensaje["usuario"], socket_cliente, id_cliente)
            self.enviar_mensaje(respuesta, socket_resp)
            respuesta["comando"] = "actualizar_lista_usuarios"  # Actualizar comando para el resto
            for user in self.usuarios:
                if user.id != id_cliente:
                    self.enviar_mensaje(respuesta, user.socket)

    def validar_login(self, usuario: str, socket_cliente, id_cliente: int) -> tuple:
        dict_respuesta = {"comando": "respuesta_validacion_login"}
        dict_respuesta["estado"] = "rechazado"
        if usuario in [user.data["usuario"] for user in self.usuarios.values()]:
            dict_respuesta["error"] = "usuario ya existe"
        elif data_json("LARGO_USUARIO_MIN") > len(usuario):
            dict_respuesta["error"] = "usuario muy corto"
        elif data_json("LARGO_USUARIO_MAX") < len(usuario):
            dict_respuesta["error"] = "usuario muy largo"
        elif not usuario.isalnum():
            dict_respuesta["error"] = "usuario no es alfanumérico"
        else:
            dict_respuesta["estado"] = "aceptado"
            if not self.usuarios:
                dict_respuesta["admin"] = True
            else:
                dict_respuesta["admin"] = False

            random.shuffle(self.colores_idx)
            color = self.colores[self.colores_idx.pop()]

            self.usuarios[id_cliente] = Usuario(usuario, socket_cliente, id_cliente, color)
            dict_respuesta["usuarios"] = [user.data for user in self.usuarios.values()]

        return (dict_respuesta, socket_cliente)

    def enviar_mensaje(self, mensaje: dict, socket_cliente) -> bool:
        self.parent.enviar_mensaje(mensaje, socket_cliente)

    def eliminar_cliente(self, id_cliente: int):
        idx = None
        for i, user in enumerate(self.usuarios):
            if user.id == id_cliente:
                idx = i

        try:
            self.usuarios.pop(idx).socket.close()
            return True
        except TypeError:
            return False


class Usuario:
    def __init__(self, usuario: str, socket_cliente, id_cliente: int, color: str):
        self.socket = socket_cliente
        self.id = id_cliente
        self.data = {
            "usuario": usuario,
            "color": color
        }
