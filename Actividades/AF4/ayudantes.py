from collections import namedtuple, defaultdict
from functools import reduce

Plato = namedtuple('nombre', 'nombre ingredientes')


class Ayudante:
    def __init__(self, nombre, platos, dinero):
        self.nombre = nombre
        self.platos = platos  # lista con namedtuples de platos
        self.dinero = dinero

    def obtener_ingredientes_platos(self) -> list:
        mapa = map(lambda x: x[1], self.platos)
        return list(mapa)

    def cantidad_ingredientes(self, lista_ingredientes_platos):
        ingredientes = {}
        for plato in lista_ingredientes_platos:
            for ingrediente in plato:
                if ingrediente[0] in ingredientes:
                    ingredientes[ingrediente[0]] += ingrediente[1]
                else:
                    ingredientes[ingrediente[0]] = ingrediente[1]

        for nombre in ingredientes:
            yield (nombre, ingredientes[nombre])

    def total_compra(self, ingredientes_platos, supermercado):
        lista_completa = reduce(lambda x, y: x + y, ingredientes_platos)
        return sum(map(lambda x: supermercado.consulta_precio(x[0]) * x[1], lista_completa))
