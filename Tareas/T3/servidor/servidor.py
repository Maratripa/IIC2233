import json
import socket
from threading import Thread, Lock
from logica import Logica
from utils import encriptar_mensaje, desencriptar_mensaje, log


class Servidor:

    lock_mensajes = Lock()

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.conectado = False
        self.id_cliente = 0

        self.logica = Logica(self)

        log("".center(80, '-'))
        log("Inicializando servidor...")
        self.iniciar_servidor()

    def iniciar_servidor(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.conectado = True

        log(f"Host: {self.host} | Port: {self.port}")
        self.comenzar_a_aceptar()

    def comenzar_a_aceptar(self):
        thread = Thread(target=self.aceptar_clientes, daemon=True)
        thread.start()

    def aceptar_clientes(self):
        while self.conectado:
            try:
                client_socket, _ = self.socket_servidor.accept()
                thread_cliente = Thread(target=self.escuchar_cliente,
                                        args=(self.id_cliente, client_socket))
                thread_cliente.start()
                self.id_cliente += 1
            except ConnectionError as e:
                self.log(e)
                return

    def escuchar_cliente(self, id_cliente: int, socket_cliente: socket.socket):
        log(f"EVENTO: Comenzando a escuchar al cliente {id_cliente}...")
        while True:
            try:
                mensaje = self.recibir_mensaje(socket_cliente)
                # log(f"DEBUG: Comando -> {mensaje['comando']}")
                self.logica.procesar_mensaje(mensaje, socket_cliente, id_cliente)
            except ConnectionError:
                self.eliminar_cliente(id_cliente, socket_cliente)
                return

    def recibir_mensaje(self, socket_cliente: socket.socket) -> dict:
        """Recibe mensajes del cliente"""
        num_bloques_bytes = socket_cliente.recv(4)
        num_bloques = int.from_bytes(num_bloques_bytes, byteorder="little")

        mensaje = bytearray()

        for _ in range(num_bloques):
            num_bloque_bytes = socket_cliente.recv(4)
            completo = int.from_bytes(socket_cliente.recv(1), byteorder="big")
            largo = int.from_bytes(socket_cliente.recv(1), byteorder="big")

            if completo:
                mensaje.extend(socket_cliente.recv(20))
            else:
                mensaje.extend(socket_cliente.recv(largo))

        if not mensaje:
            raise ConnectionError("ERROR: No se pudo leer el mensaje")

        mensaje_decodificado = self.decodificar_mensaje(bytes(mensaje))

        return mensaje_decodificado

    def enviar_mensaje(self, mensaje: dict, socket_cliente: socket.socket):
        """Envia un mensaje al cliente"""
        with self.lock_mensajes:
            bloques_mensaje = self.codificar_mensaje(mensaje)
            len_bytes = len(bloques_mensaje).to_bytes(4, byteorder="little")

            socket_cliente.sendall(len_bytes)
            for bloque in bloques_mensaje:
                socket_cliente.send(bloque)

    def codificar_mensaje(self, mensaje: dict) -> list:
        """Toma el mensaje, lo codifica y retorna una lista con los bloques y sus tamano"""
        mensaje_json = json.dumps(mensaje)
        mensaje_bytes = mensaje_json.encode("utf-8")

        mensaje_encriptado = encriptar_mensaje(mensaje_bytes)
        bloques = []
        i = 0
        while len(mensaje_encriptado) > 0:
            bloque = mensaje_encriptado[:20]
            num_bloque = i.to_bytes(4, byteorder="big")
            mensaje_encriptado = mensaje_encriptado[20:]

            if len(bloque) < 20:
                bloques.append(num_bloque + b'\x00' + len(bloque).to_bytes(1, byteorder="big") + bloque)
            else:
                bloques.append(num_bloque + b'\x01' + len(bloque).to_bytes(1, byteorder="big") + bloque)
            
            i += 1

        return bloques

    def decodificar_mensaje(self, mensaje_bytes: bytes) -> dict:
        mensaje_desencriptado = desencriptar_mensaje(mensaje_bytes)

        mensaje_json = mensaje_desencriptado.decode("utf-8")
        mensaje = json.loads(mensaje_json)

        return mensaje

    def eliminar_cliente(self, id_cliente: int, socket_cliente: socket.socket):
        log(f"EVENTO: Borrando socket del cliente {id_cliente}...")
        if not self.logica.eliminar_cliente(id_cliente):
            socket_cliente.close()  # Eliminar si no paso la ventana de inicio
