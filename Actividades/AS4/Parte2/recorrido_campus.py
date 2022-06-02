from Parte2.campus import Lugar
from collections import deque


def comprobar_chismoso(lugar: Lugar):
    # NO MODIFICAR
    for ayudante in lugar.ayudantes:
        if "Croak" in ayudante.frase:
            return True
    return False


def bfs_iterativo(inicio: Lugar, final: Lugar):
    visitados = []
    cola = deque()
    cola.append(inicio)

    while len(cola) > 0:
        nodo = cola.popleft()

        if nodo == final:
            return True

        if nodo in visitados:
            continue

        visitados.append(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    cola.append(vecino)

    return False


def dfs_iterativo(inicio: Lugar, final: Lugar):
    visitados = set()
    stack = []
    stack.append(inicio)

    while len(stack) > 0:
        nodo = stack.pop()

        if nodo == final:
            return True

        if nodo in visitados:
            continue

        visitados.add(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    stack.append(vecino)

    return False


def bfs_iterativo_largo(inicio: Lugar, final: Lugar):
    visitados = []
    cola = deque()
    cola.append(inicio)

    inicio.nivel = 1

    while len(cola) > 0:
        nodo = cola.popleft()

        if nodo == final:
            return nodo.nivel

        if nodo in visitados:
            continue

        visitados.append(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    vecino.nivel = nodo.nivel + 1
                    cola.append(vecino)

    return -1


def dfs_iterativo_largo(inicio: Lugar, final: Lugar):
    visitados = set()
    stack = []
    stack.append(inicio)

    inicio.nivel = 1

    while len(stack) > 0:
        nodo = stack.pop()

        if nodo == final:
            return nodo.nivel

        if nodo in visitados:
            continue

        visitados.add(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    vecino.nivel = nodo.nivel + 1
                    stack.append(vecino)

    return -1


def bfs_iterativo_camino(inicio: Lugar, final: Lugar):
    # Utiliza este diccionario para implementar el camino.
    # Las llaves del diccionario es UN nodo vecino (NO un listado de todos los nodos vecinos)
    # y el valor el nodo en cuestion
    padres = dict()
    padres[inicio] = None

    visitados = []
    cola = deque()
    cola.append(inicio)

    while len(cola) > 0:
        nodo = cola.popleft()

        if nodo in visitados:
            continue

        visitados.append(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    cola.append(vecino)
                    padres[vecino] = nodo

    return creador_camino(padres, final)


def dfs_iterativo_camino(inicio: Lugar, final: Lugar):
    # Utiliza este diccionario para implementar el camino.
    # Las llaves del diccionario es UN nodo vecino (NO un listado de todos los nodos vecinos)
    # y el valor el nodo en cuestion
    padres = dict()
    padres[inicio] = None

    visitados = set()
    stack = []
    stack.append(inicio)

    while len(stack) > 0:
        nodo = stack.pop()

        if nodo in visitados:
            continue

        visitados.add(nodo)

        if not comprobar_chismoso(nodo):
            for vecino in nodo.vecinos:
                if vecino not in visitados:
                    stack.append(vecino)
                    padres[vecino] = nodo

    return creador_camino(padres, final)


def creador_camino(diccionario_padres, final):
    # NO MODIFICAR
    camino = []
    camino.append(final)
    while diccionario_padres[final] is not None:
        camino.append(diccionario_padres[final])
        final = diccionario_padres[final]
    camino.reverse()
    return camino


def imprimir_camino(camino):
    # NO MODIFICAR
    recorrido = ""
    largo = len(camino)
    contador = 1
    for lugar in camino:
        if contador < largo:
            recorrido = recorrido + f"[{lugar.nombre}] -> "
        else:
            recorrido = recorrido + f"[{lugar.nombre}]."
        contador += 1
    print(recorrido)


if __name__ == "__main__":
    print("\nNO DEBES EJECUTAR AQUÍ EL PROGRAMA!!!!")
    print("Ejecuta el main.py\n")
    raise(ModuleNotFoundError)
