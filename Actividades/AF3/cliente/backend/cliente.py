"""
Modulo contiene implementación principal del cliente
"""
from optparse import IndentedHelpFormatter
import socket
import json
from threading import Thread
from backend.interfaz import Interfaz


class Cliente:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conectado = False
        self.interfaz = Interfaz(self)
        self.iniciar_cliente()

    def iniciar_cliente(self):
        """
        Se encarga de iniciar el cliente y conectar el socket
        """

        # TODO: Completado por estudiante
        try:
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True
            self.comenzar_a_escuchar()
            self.interfaz.mostrar_ventana_carga()

        except ConnectionError as e:
            print(e)

    def comenzar_a_escuchar(self):
        """
        Instancia el Thread que escucha los mensajes del servidor
        """
        # TODO: Completado por estudiante
        thread = Thread(target=self.escuchar_servidor, daemon=True)
        thread.start()

    def escuchar_servidor(self):
        """
        Recibe mensajes constantes desde el servidor y responde.
        """
        # TODO: Completado por estudiante
        while self.conectado:
            try:
                mensaje = self.recibir()
                self.interfaz.manejar_mensaje(mensaje)
            except ConnectionError as e:
                print(e)

    def recibir(self):
        """
        Se encarga de recibir los mensajes del servidor.
        """
        # TODO: Completado por estudiante
        msg_bytes_len = self.socket_cliente.recv(4)
        msg_len = int.from_bytes(msg_bytes_len, byteorder="little")

        mensaje_bytes = bytearray()

        while len(mensaje_bytes) < msg_len:
            read_len = min(64, msg_len - len(mensaje_bytes))
            mensaje_bytes.extend(self.socket_cliente.recv(read_len))

        mensaje_decodificado = self.decodificar_mensaje(mensaje_bytes)

        return mensaje_decodificado

    def enviar(self, mensaje: dict):
        """
        Envía un mensaje a un cliente.
        """
        # TODO: Completado por estudiante
        mensaje_codificado = self.codificar_mensaje(mensaje)
        msg_len_bytes = len(mensaje_codificado).to_bytes(4, byteorder="little")

        self.socket_cliente.sendall(msg_len_bytes + mensaje_codificado)

    def codificar_mensaje(self, mensaje: dict):
        """
        Codifica el mensaje a enviar
        """
        try:
            # TODO: Completado por estudiante
            mensaje_json = json.dumps(mensaje)
            mensaje_codificado = mensaje_json.encode("utf-8")

            return mensaje_codificado
        except json.JSONDecodeError:
            print("ERROR: No se pudo codificar el mensaje")
            return b""

    def decodificar_mensaje(self, mensaje_bytes: bytes):
        """
        Decodifica el mensaje del servidor
        """
        try:
            # TODO: Completado por estudiante
            mensaje_json = mensaje_bytes.decode("utf-8")
            mensaje_decodificado = json.loads(mensaje_json)

            return mensaje_decodificado
        except json.JSONDecodeError:
            print("ERROR: No se pudo decodificar el mensaje")
            return {}
