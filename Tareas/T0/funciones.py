from typing import List


def manejo_errores(callback, previous, mensaje=""):
    print(mensaje)
    print("Por favor elija una opcion:")
    print("[1] Reintentar")
    print("[2] Volver")

    opcion = manejo_opciones(2)

    if opcion == 1:
        callback()
    elif opcion == 2:
        previous()


def manejo_opciones(max_op, mensaje=""):
    print(mensaje)
    opcion = input("Ingrese la opcion elegida: ")

    if opcion.isnumeric():
        opcion = int(opcion)
    else:
        return manejo_opciones(max_op, "Opcion no es un numero")

    if opcion > max_op:
        return manejo_opciones(max_op, "Opcion no disponible")

    return opcion


def mostrar_encomiendas(encomiendas: list) -> None:
    for i in range(len(encomiendas)):
        act = encomiendas[i]
        print(f"{i + 1}) {act.nombre}")


def cambiar_estado(encomienda):
    if encomienda.estado == "Emitida":
        return "Revisada por agencia"
    elif encomienda.estado == "Revisada por agencia":
        return "En camino"
    elif encomienda.estado == "En camino":
        return "Llegada al destino"
    elif encomienda.estado == "Llegada al destino":
        return encomienda.estado
    else:
        return None
