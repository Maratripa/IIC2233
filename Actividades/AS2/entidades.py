from abc import ABC, abstractmethod
from random import randint
from threading import Thread, Lock, Event, Timer
from time import sleep


class Persona(ABC, Thread):

    # Completar
    lock_bodega = Lock()
    lock_cola_pedidos = Lock()
    lock_cola_pedidos_listos = Lock()

    def __init__(self, nombre):
        super().__init__()
        self.nombre = nombre
        self.disponible = True
        self.trabajando = True
        self.daemon = True

    @abstractmethod
    def run(self):
        pass


class Cocinero(Persona):

    def __init__(self, nombre, cocina):
        super().__init__(nombre)
        self.lugar_trabajo = cocina
        # Completar
        self.evento_plato_asignado = Event()

    def run(self) -> None:
        # Completar
        while self.trabajando:
            self.evento_plato_asignado.wait()

            tiempo_espera = randint(1, 3)
            sleep(tiempo_espera)
            self.cocinar()

    def cocinar(self):
        # Completar
        self.disponible = False
        plato = self.sacar_plato()
        print(f"El cocinero {self.nombre} esta cocinando {plato[1]}")

        self.buscar_ingredientes(
            plato, self.lugar_trabajo.bodega, self.lugar_trabajo.recetas)

        tiempo_espera = randint(1, 3)
        sleep(tiempo_espera)

        self.agregar_plato(plato)

        self.evento_plato_asignado.clear()

        self.disponible = True

    def sacar_plato(self) -> tuple:
        # Completar
        with self.lock_cola_pedidos:
            plato = self.lugar_trabajo.cola_pedidos.popleft()

            return plato

    def buscar_ingredientes(self, plato: tuple, bodega: dict, recetas: dict):
        # Formato de los dicts entregados:
        # bodega = {
        #     "alimento_1": int cantidad_alimento_1,
        #     "alimento_2": int cantidad_alimento_2,
        # }
        # recetas = {
        #     "nombre_plato_1": [("ingrediente_1", "cantidad_ingrediente_1"),
        #                        ("ingrediente_2", "cantidad_ingrediente_2")],
        #     "nombre_plato_2": [("ingrediente_1", "cantidad_ingrediente_1"),
        #                        ("ingrediente_2", "cantidad_ingrediente_2")]
        # }

        # Completar
        nombre_plato = plato[0]

        print(f"Buscando ingredientes para el plato {nombre_plato}...")

        ingredientes = recetas[nombre_plato]

        for i in ingredientes:
            with self.lock_bodega:
                nombre_ing = i[0]
                cantidad = int(i[1])

                print(f"Sacando {cantidad} de {nombre_ing}...")

                bodega[nombre_ing] -= cantidad

    def agregar_plato(self, plato):
        # Completar
        pass


class Mesero(Persona):

    def __init__(self, nombre):
        super().__init__(nombre)
        # Completar

    def run(self):
        # Completar
        pass

    def agregar_pedido(self, pedido, cocina):
        # Completar
        pass

    def entregar_pedido(self, cocina):
        # Completar
        pass

    def pedido_entregado(self, pedido):
        # Completar
        pass
