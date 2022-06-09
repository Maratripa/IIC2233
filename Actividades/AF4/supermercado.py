class Pasillo:
    def __init__(self, id, nombre, productos=None):
        if productos is None:
            productos = []
        self.id = id
        self.nombre = nombre
        self.productos = productos  # lista con los nombres de los productos que hay en el pasillo
        self.siguiente = None

    def __repr__(self):
        return self.nombre


class ListaPasillos:
    def __init__(self, primer_pasillo):
        self.primer_pasillo = primer_pasillo

    def __iter__(self):
        return IteradorPasillos(self.primer_pasillo)


class IteradorPasillos:
    def __init__(self, primer_pasillo):
        self.pasillo = primer_pasillo

    def __iter__(self):
        return self

    def __next__(self):
        if self.pasillo == None:
            raise StopIteration("Final de los pasillos")
        else:
            valor = self.pasillo
            self.pasillo = self.pasillo.siguiente
            return valor


class Supermercado:
    def __init__(self, lista_pasillos, productos):
        self.pasillos = lista_pasillos  # lista ligada de pasillos (primer elemento)
        self.productos = productos  # dict {"nombre ingrediente": (pasillo.id, precio)}

    def consulta_precio(self, nombre_producto):
        return self.productos[nombre_producto][1]

    def pasillo_tiene_ingredientes(self, pasillo, ingredientes_platos):
        for plato in ingredientes_platos:
            for ingrediente in plato:
                if ingrediente[0] in pasillo.productos:
                    return True
        return False

    def pasillos_a_recorrer(self, ingredientes_platos):
        return filter(lambda x: self.pasillo_tiene_ingredientes(x, ingredientes_platos), self.pasillos)
