import os

import entidades
from jugador import JugadorTacano, JugadorBebedor, JugadorLudopata, JugadorCasual


def obtener_jugadores() -> list:
    # path de este archivo y de aqui ir a los csv
    dir_path = os.path.dirname(os.path.realpath(__file__))

    jugadores = []  # lista con instancias de jugadores

    with open(os.path.join(dir_path, "jugadores.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')  # llaves del diccionario

        for line in lectura[1:]:
            actual = {headers[i]: e for
                      i, e in enumerate(line.strip().split(','))}  # comprension de diccionarios

            entry = {  # diccionario de kwargs para los jugadores
                "nombre": actual["nombre"],
                "personalidad": actual["personalidad"],
                "energia": actual["energia"],
                "suerte": actual["suerte"],
                "dinero": actual["dinero"],
                "frustracion": actual["frustracion"],
                "ego": actual["ego"],
                "carisma": actual["carisma"],
                "confianza": actual["confianza"],
                "juego_favorito": actual["juego favorito"]
            }

            if actual["personalidad"] == "Ludopata":
                jugadores.append(JugadorLudopata(**entry))

            elif actual["personalidad"] == "Tacano":
                jugadores.append(JugadorTacano(**entry))

            elif actual["personalidad"] == "Bebedor":
                jugadores.append(JugadorBebedor(**entry))

            elif actual["personalidad"] == "Casual":
                jugadores.append(JugadorCasual(**entry))

    return jugadores  # lista de jugadores


def obtener_bebestibles() -> list:
    # path de este archivo y de aqui ir a los csv
    dir_path = os.path.dirname(os.path.realpath(__file__))

    bebestibles = []

    with open(os.path.join(dir_path, "bebestibles.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')  # llaves del diccionario

        for line in lectura[1:]:
            actual = {headers[i]: e for i,
                      e in enumerate(line.strip().split(','))}  # comprension de diccionario

            if actual["tipo"] == "Jugo":
                bebestibles.append(entidades.Jugo(**actual))

            elif actual["tipo"] == "Gaseosa":
                bebestibles.append(entidades.Gaseosa(**actual))

            elif actual["tipo"] == "Brebaje mágico":
                bebestibles.append(entidades.BrebajeMagico(**actual))

    return bebestibles  # lista de bebestibles


def obtener_juegos() -> list:
    # path de este archivo y de aqui ir a los csv
    dir_path = os.path.dirname(os.path.realpath(__file__))

    juegos = []

    with open(os.path.join(dir_path, "juegos.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')  # llaves del diccionario

        for line in lectura[1:]:
            actual = {headers[i]: e for i,
                      e in enumerate(line.strip().split(','))}  # comprension de diccionario

            # kwargs de juegos
            entry = {
                "nombre": actual["nombre"],
                "esperanza": actual["esperanza"],
                "ap_min": actual["apuesta minima"],
                "ap_max": actual["apuesta maxima"]
            }

            juegos.append(entidades.Juego(**entry))

    return juegos  # lista de juegos
