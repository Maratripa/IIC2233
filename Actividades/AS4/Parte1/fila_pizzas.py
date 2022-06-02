class Cliente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.siguiente = None

    def __str__(self):
        # NO MODIFICAR
        return self.nombre


class FilaPizza:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.largo = 0

    def llega_cliente(self, cliente: Cliente):
        if self.largo == 0:
            self.primero = cliente
            self.ultimo = cliente
            self.largo += 1
        else:
            self.ultimo.siguiente = cliente
            self.ultimo = cliente
            self.largo += 1

    def alguien_se_cuela(self, cliente: Cliente, posicion: int):
        if self.largo == 0:
            self.primero = cliente
            self.ultimo = cliente
            self.largo += 1
        elif posicion == 0:
            cliente.siguiente = self.primero
            self.primero = cliente
            self.largo += 1
        elif posicion >= self.largo:
            self.llega_cliente(cliente)
        else:
            tmp = self.primero
            for i in range(posicion - 1):
                tmp = tmp.siguiente
            cliente.siguiente = tmp.siguiente
            tmp.siguiente = cliente
            self.largo += 1

    def cliente_atendido(self) -> Cliente:
        if self.largo == 1:
            cliente = self.primero
            self.primero = None
            self.ultimo = None
            self.largo -= 1
            return cliente
        elif self.largo > 1:
            cliente = self.primero
            self.primero = self.primero.siguiente
            self.largo -= 1
            return cliente

    def __str__(self):
        string = self.primero.__str__()
        tmp = self.primero.siguiente
        for _ in range(self.largo - 1):
            string += " -> " + tmp.__str__()
            tmp = tmp.siguiente

        return string


if __name__ == "__main__":
    print("\nNO DEBES EJECUTAR AQUÍ EL PROGRAMA!!!!")
    print("Ejecuta el main.py\n")
    raise(ModuleNotFoundError)
