import random
from utils import data_json, log


class Logica:
    def __init__(self, parent):
        self.parent = parent

        self.usuarios = []
        self.turno = 0

        self.colores = ("rojo", "amarillo", "azul", "verde")
        self.colores_idx = [0, 1, 2, 3]
        random.shuffle(self.colores_idx)

    def procesar_mensaje(self, mensaje: dict, socket_cliente, id_cliente: int) -> None:
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "validar_login":
            respuesta, socket_resp = self.validar_login(mensaje["usuario"], socket_cliente,
                                                        id_cliente)
            self.enviar_mensaje(respuesta, socket_resp)

            # Actualizar comando para el resto si el usuario fue aceptado
            if respuesta["estado"] == "aceptado":
                respuesta["comando"] = "actualizar_lista_usuarios"
                for user in self.usuarios:
                    if user.id != id_cliente:
                        self.enviar_mensaje(respuesta, user.socket)

        elif comando == "iniciar_partida":
            respuesta = {"comando": "repuesta_iniciar_partida"}
            if not (data_json("MINIMO_JUGADORES") <= len(mensaje["usuarios"])) and (
                    len(mensaje["usuarios"]) <= data_json("MAXIMO_JUGADORES")):
                respuesta["estado"] = "rechazado"
                respuesta["error"] = "numero de usuarios no valido"
            else:
                respuesta["estado"] = "aceptado"
                respuesta["usuarios"] = mensaje["usuarios"]

            for user in self.usuarios:
                self.enviar_mensaje(respuesta, user.socket)

            self.actualizar_juego()

        elif comando == "tirar_dado":
            pass

    def validar_login(self, usuario: str, socket_cliente, id_cliente: int) -> tuple:
        dict_respuesta = {"comando": "respuesta_validacion_login"}
        dict_respuesta["estado"] = "rechazado"
        if usuario in [user.data["usuario"] for user in self.usuarios]:
            dict_respuesta["error"] = "usuario ya existe"
        elif data_json("LARGO_USUARIO_MIN") > len(usuario):
            dict_respuesta["error"] = "usuario muy corto"
        elif data_json("LARGO_USUARIO_MAX") < len(usuario):
            dict_respuesta["error"] = "usuario muy largo"
        elif not usuario.isalnum():
            dict_respuesta["error"] = "usuario no es alfanumérico"
        elif len(self.usuarios) == data_json("MAXIMO_JUGADORES"):
            dict_respuesta["error"] = "sala llena"
        else:
            dict_respuesta["estado"] = "aceptado"
            if not self.usuarios:
                dict_respuesta["admin"] = True
            else:
                dict_respuesta["admin"] = False

            color_i = self.colores_idx.pop(0)
            self.colores_idx.append(color_i)

            self.usuarios.append(Usuario(usuario, socket_cliente,
                                 id_cliente, self.colores[color_i]))
            dict_respuesta["usuarios"] = [user.data for user in self.usuarios]

        return (dict_respuesta, socket_cliente)

    def actualizar_juego(self):
        jugador_actual = self.usuarios[self.turno % len(self.usuarios)]
        lanzamiento = random.randint(*data_json("RANGO_DADO"))

        log(f"El jugador {jugador_actual.data['usuario']} ha lanzado el numero {lanzamiento}")

        self.turno += 1
        respuesta = {
            "comando": "actualizar_juego",
            "en_turno": True,
            "num_dado": lanzamiento
        }
        jugador_nuevo = self.usuarios[self.turno % len(self.usuarios)]
        self.enviar_mensaje(respuesta, jugador_nuevo.socket)
        respuesta["en_turno"] = False
        for user in self.usuarios:
            if user != jugador_nuevo:
                self.enviar_mensaje(respuesta, user.socket)

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
