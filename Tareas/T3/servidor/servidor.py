import socket
from threading import Thread


class Servidor:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket_servidor = None
        self.conectado = False
        self.id_cliente = 0

        self.log("".center(80, '-'))
        self.log("Inicializando servidor...")
        self.iniciar_servidor()

    def iniciar_servidor(self):
        self.socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_servidor.bind((self.host, self.port))
        self.socket_servidor.listen()
        self.conectado = True

        self.log("Host: %s | Port: %d" % (self.host, self.port))
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
        self.log("Comenzando a escuchar al cliente %d..." % id_cliente)
        while True:
            try:
                mensaje = socket_cliente.recv(1)
                if not mensaje:
                    raise ConnectionError()
            except ConnectionError:
                self.eliminar_cliente(id_cliente, socket_cliente)
                return

    def eliminar_cliente(self, id_cliente: int, socket_cliente: socket.socket):
        self.log("Borrando socket del cliente %d..." % id_cliente)
        socket_cliente.close()

    def log(self, mensaje):
        """Imprime un mensaje en consola"""
        print("|" + mensaje.center(80, " ") + "|")
