import json
import socket
import threading

from backend.interfaz import Interfaz
from utils import desencriptar_mensaje, encriptar_mensaje


class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False

        self.interfaz = Interfaz(self)

        self.iniciar_cliente()

    def iniciar_cliente(self):
        """Iniciar cliente y conectar socket"""
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.log("Cliente inicializado")
            self.comenzar_a_escuchar()
            self.interfaz.mostrar_ventana_inicio()

        except ConnectionError as e:
            self.log(e)

    def comenzar_a_escuchar(self):
        """Instancia el Thread que escucha mensajes"""
        thread = threading.Thread(target=self.escuchar_servidor, daemon=True)
        thread.start()

    def escuchar_servidor(self):
        """Recibe mensajes desde el servidor y responde"""
        self.log("Escuchando servidor")
        while self.conectado:
            try:
                mensaje = self.recibir_mensaje()
                self.log(mensaje.__str__())
                respuesta = self.interfaz.procesar_mensaje(mensaje)
            except ConnectionError as e:
                self.log(e.__str__())
                return

    def enviar_mensaje(self, mensaje: dict):
        """Envia un mensaje al servidor"""
        bloques_mensaje = self.codificar_mensaje(mensaje)
        len_bytes = len(bloques_mensaje).to_bytes(4, byteorder="little")

        self.socket_cliente.sendall(len_bytes)
        for bloque in bloques_mensaje:
            self.socket_cliente.sendall(bloque)

    def recibir_mensaje(self) -> dict:
        """Recibe mensajes del servidor"""
        num_bloques_bytes = self.socket_cliente.recv(4)
        num_bloques = int.from_bytes(num_bloques_bytes, byteorder="little")

        mensaje = bytearray()

        for _ in range(num_bloques):
            num_bloque_bytes = self.socket_cliente.recv(4)
            mensaje.extend(self.socket_cliente.recv(22))

        if not mensaje:
            raise ConnectionError("ERROR: Could not read message")

        mensaje_decodificado = self.decodificar_mensaje(bytes(mensaje))

        return mensaje_decodificado

    def codificar_mensaje(self, mensaje: dict) -> list:
        """Toma el mensaje, lo codifica y retorna una lista con los bloques y sus tamano"""
        mensaje_json = json.dumps(mensaje)
        mensaje_bytes = mensaje_json.encode("utf-8")

        mensaje_encriptado = encriptar_mensaje(mensaje_bytes)
        bloques = []

        while len(mensaje_encriptado) > 0:
            bloque = mensaje_encriptado[:22]
            num_bloque = len(bloque).to_bytes(4, byteorder="big")
            bloques.append(num_bloque + bloque)
            mensaje_encriptado = mensaje_encriptado[22:]

        return bloques

    def decodificar_mensaje(self, mensaje_bytes: bytes) -> dict:
        mensaje_desencriptado = desencriptar_mensaje(mensaje_bytes)

        mensaje_json = mensaje_desencriptado.decode("utf-8")
        mensaje = json.loads(mensaje_json)

        return mensaje

    def log(self, mensaje: str):
        """Imprime un mensaje en la consola"""
        print('|' + mensaje.center(80, ' ') + '|')
