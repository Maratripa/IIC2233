import random
from utils import data_json


class Logica:
    def __init__(self, parent):
        self.parent = parent

        self.usuarios = []

        self.colores = ("rojo", "amarillo", "azul", "verde")
        self.colores_idx = [0, 1, 2, 3]

    def procesar_mensaje(self, mensaje: dict, socket_cliente, id_cliente: int) -> dict:
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "validar_login":
            respuesta = self.validar_login(mensaje["usuario"], id_cliente)

        return respuesta

    def validar_login(self, usuario: str, id_cliente: int) -> dict:
        dict_respuesta = {"comando": "respuesta_validacion_login"}
        if usuario in [user["usuario"] for user in self.usuarios]:
            dict_respuesta["estado"] = "rechazado"
            dict_respuesta["error"] = "usuario ya existe"
        elif data_json("LARGO_USUARIO_MIN") > len(usuario):
            dict_respuesta["estado"] = "rechazado"
            dict_respuesta["error"] = "usuario muy corto"
        elif data_json("LARGO_USUARIO_MAX") < len(usuario):
            dict_respuesta["estado"] = "rechazado"
            dict_respuesta["error"] = "usuario muy largo"
        elif not usuario.isalnum():
            dict_respuesta["estado"] = "rechazado"
            dict_respuesta["error"] = "usuario no es alfanumérico"
        else:
            dict_respuesta["estado"] = "aceptado"
            if not self.usuarios:
                dict_respuesta["admin"] = True
            else:
                dict_respuesta["admin"] = False

            random.shuffle(self.colores_idx)
            color = self.colores[self.colores_idx.pop()]

            self.usuarios.append({
                "usuario": usuario,
                "color": color,
            })
            dict_respuesta["usuarios"] = self.usuarios

        return dict_respuesta
