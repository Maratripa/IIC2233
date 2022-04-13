import os

import entidades


def obtener_jugadores() -> list:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    jugadores = []  # lista con instancias de jugadores

    with open(os.path.join(dir_path, "jugadores.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')

        for line in lectura[1:]:
            actual = {headers[i]: e for
                      i, e in enumerate(line.strip().split(','))}
            entry = {
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
                jugadores.append(entidades.JugadorLudopata(**entry))

            elif actual["personalidad"] == "Tacano":
                jugadores.append(entidades.JugadorTacano(**entry))

            elif actual["personalidad"] == "Bebedor":
                jugadores.append(entidades.JugadorBebedor(**entry))

            elif actual["personalidad"] == "Casual":
                jugadores.append(entidades.JugadorCasual(**entry))

    return jugadores


def obtener_bebestibles() -> list:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    bebestibles = []

    with open(os.path.join(dir_path, "bebestibles.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')

        for line in lectura[1:]:
            actual = {headers[i]: e for i,
                      e in enumerate(line.strip().split(','))}

            if actual["tipo"] == "Jugo":
                bebestibles.append(entidades.Jugo(**actual))

            elif actual["tipo"] == "Gaseosa":
                bebestibles.append(entidades.Gaseosa(**actual))

            elif actual["tipo"] == "Brebaje mágico":
                bebestibles.append(entidades.BrebajeMagico(**actual))

    return bebestibles


def obtener_juegos() -> list:
    dir_path = os.path.dirname(os.path.realpath(__file__))

    juegos = []

    with open(os.path.join(dir_path, "juegos.csv"), 'r', encoding="utf-8") as file:
        lectura = file.readlines()

        headers = lectura[0].strip().split(',')

        for line in lectura[1:]:
            actual = {headers[i]: e for i,
                      e in enumerate(line.strip().split(','))}

            entry = {
                "nombre": actual["nombre"],
                "esperanza": actual["esperanza"],
                "ap_min": actual["apuesta minima"],
                "ap_max": actual["apuesta maxima"]
            }

            juegos.append(entidades.Juego(**entry))

    return juegos
