import socket
import threading

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
            pass

    def log(self, mensaje: str):
        """Imprime un mensaje en la consola"""
        print('|' + mensaje.center(80, ' ') + '|')
