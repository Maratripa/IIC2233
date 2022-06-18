import random
from utils import data_json, log


class Logica:
    def __init__(self, parent):
        self.parent = parent

        self.usuarios = []
        self.turno = 0

        self.colores = ["rojo", "amarillo", "azul", "verde"]
        random.shuffle(self.colores)

    def procesar_mensaje(self, mensaje: dict, socket_cliente, id_cliente: int) -> None:
        try:
            comando = mensaje["comando"]
        except KeyError:
            return {}

        if comando == "validar_login":
            respuesta = self.validar_login(mensaje["usuario"], socket_cliente,
                                           id_cliente)
            self.enviar_mensaje(respuesta, socket_cliente)

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

            if respuesta["estado"] == "aceptado":
                self.iniciar_juego()

        elif comando == "tirar_dado":
            self.actualizar_juego()

    def validar_login(self, usuario: str, socket_cliente, id_cliente: int) -> dict:
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

            color = self.colores.pop(0)
            self.colores.append(color)

            self.usuarios.append(Usuario(usuario, socket_cliente,
                                 id_cliente, color))
            dict_respuesta["usuarios"] = [user.data for user in self.usuarios]

        return dict_respuesta

    def iniciar_juego(self):
        self.turno = 0
        log(f"EVENTO: Comienza la partida con {len(self.usuarios)} jugadores")
        for user in self.usuarios:
            log(f"EVENTO: {user.data['usuario']} se une a la partida")

        posiciones = {}
        for user in self.usuarios:
            posiciones[user.data['color']] = user.pos
            log(f"DEBUG: Posicion inicial jugador {user.data['usuario']} es {user.pos}")

        respuesta = {
            "comando": "actualizar_juego",
            "en_turno": True,
            "nombre_en_turno": self.usuarios[0].data["usuario"],
            "num_dado": '?',
            "posiciones": posiciones
        }
        self.enviar_mensaje(respuesta, self.usuarios[0].socket)
        respuesta["en_turno"] = False
        for user in self.usuarios:
            if user != self.usuarios[0]:
                self.enviar_mensaje(respuesta, user.socket)

    def actualizar_juego(self):
        actual = self.usuarios[self.turno % len(self.usuarios)]
        lanzamiento = random.randint(*data_json("RANGO_DADO"))

        nueva_pos = actual.avanzar_jugador(lanzamiento)

        log(f"EVENTO: El jugador {actual.data['usuario']} ha lanzado el numero {lanzamiento}")
        log(f"EVENTO: El jugador {actual.data['usuario']} se ha movido a {actual.pos}")

        self.turno += 1
        jugador_nuevo = self.usuarios[self.turno % len(self.usuarios)]
        respuesta = {
            "comando": "actualizar_juego",
            "en_turno": True,
            "nombre_en_turno": jugador_nuevo.data["usuario"],
            "num_dado": lanzamiento,
            "posiciones": nueva_pos,
        }
        self.enviar_mensaje(respuesta, jugador_nuevo.socket)
        respuesta["en_turno"] = False
        for user in self.usuarios:
            if user != jugador_nuevo:
                self.enviar_mensaje(respuesta, user.socket)

        hay_ganador = False
        ganador = None
        for user in self.usuarios:
            if user.avanzados == 22:
                hay_ganador = True
                ganador = user

        if hay_ganador:
            self.terminar_juego(ganador)

    def terminar_juego(self, ganador):
        respuesta = {
            "comando": "terminar_juego",
            "ganador": ganador.data['usuario'],
            "usuarios": [user.data for user in self.usuarios]
        }

        for user in self.usuarios:
            self.parent.enviar_mensaje(respuesta, user.socket)

    def enviar_mensaje(self, mensaje: dict, socket_cliente) -> bool:
        self.parent.enviar_mensaje(mensaje, socket_cliente)

    def eliminar_cliente(self, id_cliente: int):
        idx = None
        for i, user in enumerate(self.usuarios):
            if user.id == id_cliente:
                idx = i

        try:
            color = self.usuarios[idx].data['color']
            self.colores.insert(0, color)
            self.usuarios.pop(idx).socket.close()
            for user in self.usuarios:
                self.enviar_mensaje({"comando": "actualizar_lista_usuarios",
                                     "usuarios": [user.data for user in self.usuarios]},
                                    user.socket)
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

        self.avanzados = 0

        if color == "azul":
            self.dir = 0
            self.pos = [0, 0]
        elif color == "amarillo":
            self.dir = 1
            self.pos = [0, 5]
        elif color == "verde":
            self.dir = 2
            self.pos = [5, 5]
        elif color == "rojo":
            self.dir = 3
            self.pos = [5, 0]

    def avanzar_jugador(self, numero) -> dict:
        if self.avanzados + numero < 23:
            for _ in range(numero):
                if self.avanzados != 0:
                    self.cambiar_direccion()

                if self.dir == 0:
                    self.pos[1] += 1
                elif self.dir == 1:
                    self.pos[0] += 1
                elif self.dir == 2:
                    self.pos[1] -= 1
                elif self.dir == 3:
                    self.pos[0] -= 1
                self.avanzados += 1

        return {self.data['color']: self.pos}

    def cambiar_direccion(self):
        if self.avanzados % 5 == 0 and self.avanzados < 19:
            self.dir = (self.dir + 1) % 4
        elif self.avanzados == 19:
            self.dir = (self.dir + 1) % 4
