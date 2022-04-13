from abc import ABC, abstractmethod
import random

import parametros
from jugador import Jugador, JugadorBebedor, JugadorCasual, JugadorLudopata, JugadorTacano


class Juego:

    def __init__(self, nombre, esperanza, ap_min, ap_max, *ar, **kw):
        self.nombre = nombre
        self.esperanza = int(esperanza)
        self.apuesta_minima = int(ap_min)
        self.apuesta_maxima = int(ap_max)

    def entregar_resultados(self, jugador: Jugador, apuesta: int, gano: bool) -> None:
        if gano:
            jugador.ego += parametros.EGO_GANAR
            jugador.carisma += parametros.CARISMA_GANAR
            jugador.frustracion -= parametros.FRUSTRACION_GANAR

            print(
                f"\nJugando {self.nombre}, el jugador {jugador.nombre} ha ganado ${apuesta * 2:,}")
            jugador.dinero += apuesta * 2

        else:
            jugador.frustracion += parametros.FRUSTRACION_PERDER
            jugador.confianza -= parametros.CONFIANZA_PERDER

            print(
                f"\nJugando {self.nombre}, el jugador {jugador.nombre} ha perdido ${apuesta:,}")
            jugador.dinero -= apuesta

    def probabilidad_de_ganar(self, jugador: Jugador, apuesta: int) -> float:
        prob = min(
            1, max(0, (jugador.probabilidad_ganar(self.nombre, apuesta) -
                       ((apuesta - (self.es_favorito(jugador) * 50
                        - (self.esperanza * 30))) / float(10_000)))))

        return prob

    def es_favorito(self, jugador: Jugador) -> bool:
        if self.nombre == jugador.juego_favorito:
            return 1
        else:
            return 0

    def menu_de_juego(self, jugador: Jugador):

        def print_menu() -> int:
            titulo = f"*** {self.nombre} ***"
            print(f"\n\n{titulo: ^37s}")
            print('-' * 37)
            print(
                f"Apuesta mínima: ${self.apuesta_minima:,} |" +
                f" Apuesta máxima: ${self.apuesta_maxima:,}\n"
            )
            print(f"Dinero jugador: ${jugador.dinero:,}")

            monto = input("\nIngrese monto de apuesta ($0 para volver): $")

            if monto.isnumeric():
                monto = int(monto)
                if monto == 0:
                    return 0
                elif self.apuesta_minima <= monto <= self.apuesta_maxima and monto <= jugador.dinero:
                    return monto
                else:
                    return print_menu()
            else:
                return print_menu()

        apuesta = print_menu()

        if apuesta == 0:
            return

        jugador.apostar(self, apuesta)


class Bebestible(ABC):

    def __init__(self, nombre, tipo, precio, *ar, **kw):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = int(precio)

    @abstractmethod
    def consumir(self, jugador: Jugador, multiplicador: float = 1.0) -> None:
        recuperacion = random.randint(
            parametros.MIN_ENERGIA_BEBESTIBLE, parametros.MAX_ENERGIA_BEBESTIBLE)

        recuperacion = round(recuperacion * multiplicador)
        jugador.energia += recuperacion
        print(
            f"\nEl jugador {jugador.nombre} ha recuperado {recuperacion} energía!\n")


class Jugo(Bebestible):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador, multiplicador: float = 1.0) -> None:
        super().consumir(jugador, multiplicador)

        if len(self.nombre) <= 4:
            ego = round(4 * multiplicador)
            jugador.ego += ego
            print(
                f"El ego del jugador {jugador.nombre} ha aumentado en {ego}!")

        elif 5 <= len(self.nombre) <= 7:
            suerte = round(7 * multiplicador)
            jugador.suerte += suerte
            print(
                f"La suerte del jugador {jugador.nombre} ha aumentado en {suerte}!")

        elif 8 <= len(self.nombre):
            frustracion = round(10 * multiplicador)
            ego = round(11 * multiplicador)
            jugador.frustracion -= frustracion
            jugador.ego += ego
            print(f"La frustración del jugador {jugador.nombre} ha disminuído " +
                  f"en {frustracion}, pero el ego ha aumentado en {ego}!")


class Gaseosa(Bebestible):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador, multiplicador: float = 1.0) -> None:
        super().consumir(jugador, multiplicador)

        if isinstance(jugador, JugadorTacano) or isinstance(jugador, JugadorLudopata):
            frustracion = round(5 * multiplicador)
            jugador.frustracion -= frustracion
            print(
                f"La frustración del jugador {jugador.nombre} ha disminuído en {frustracion}!")

        elif isinstance(jugador, JugadorBebedor) or isinstance(jugador, JugadorCasual):
            frustracion = round(5 * multiplicador)
            jugador.frustracion += frustracion
            print(
                f"La frustración del jugador {jugador.nombre} ha aumentado en {frustracion}!")

        ego = round(6 * multiplicador)
        jugador.ego += ego
        print(f"El ego del jugador {jugador.nombre} ha aumentado en {ego}!")


class BrebajeMagico(Jugo, Gaseosa):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador, multiplicador: float = 1.0) -> None:
        super().consumir(jugador, multiplicador)

        carisma = round(5 * multiplicador)
        jugador.carisma += carisma
        print(
            f"\nEl carisma del jugador {jugador.nombre} ha aumento en {carisma}!")
