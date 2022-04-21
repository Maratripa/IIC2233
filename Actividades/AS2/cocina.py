from collections import deque
from entidades import Cocinero, Mesero
from time import sleep
from random import randint


class Cocina:

    def __init__(self, bodega, recetas):
        super().__init__()
        self.cola_pedidos = deque()
        self.cola_pedidos_listos = deque()
        self.cocineros = []
        self.meseros = []
        self.bodega = bodega
        self.recetas = recetas
        self.abierta = True

    def initialize_threads(self):
        # Completar
        for mesero in self.meseros:
            mesero.start()

        for cocinero in self.cocineros:
            cocinero.start()

    def asignar_cocinero(self):
        # Completar
        while self.abierta:
            sleep(1)

            for cocinero in self.cocineros:
                if len(self.cola_pedidos) > 0 and cocinero.disponible:
                    cocinero.evento_plato_asignado.set()

                    while cocinero.evento_plato_asignado.is_set():
                        pass

    def asignar_mesero(self):
        # Completar
        while self.abierta:
            sleep(1)

            for mesero in self.meseros:
                if len(self.cola_pedidos_listos) > 0 and mesero.disponible:
                    mesero.evento_manejar_pedido.set()
                    mesero.entregar_pedido(self)

        self.finalizar_jornada_laboral()

    def finalizar_jornada_laboral(self):
        for mesero in self.meseros:
            mesero.trabajando = False

        for cocinero in self.cocineros:
            cocinero.trabajando = False
