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

            if len(self.cola_pedidos) > 0:
                encontrado = False
                counter = 0

                while not encontrado:
                    if self.cocineros[counter].disponible:
                        encontrado = True
                        self.cocineros[counter].evento_plato_asignado.set()
                    else:
                        if counter == len(self.cocineros) - 1:
                            counter = 0
                        else:
                            counter += 1

    def asignar_mesero(self):
        # Completar
        while self.abierta:
            sleep(1)

            if len(self.cola_pedidos_listos) > 0:
                encontrado = False
                counter = 0

                while not encontrado:
                    if self.meseros[counter].disponible:
                        encontrado = True
                        self.meseros[counter].evento_manejar_pedido.set()
                        self.meseros[counter].entregar_pedido(self)
                    else:
                        if counter == len(self.meseros) - 1:
                            counter = 0
                        else:
                            counter += 1

        self.finalizar_jornada_laboral()

    def finalizar_jornada_laboral(self):
        for mesero in self.meseros:
            mesero.trabajando = False

        for cocinero in self.cocineros:
            cocinero.trabajando = False
