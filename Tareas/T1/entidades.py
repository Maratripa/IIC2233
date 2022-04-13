from abc import ABC, abstractmethod
import random

import parametros


class Jugador(ABC):

    def __init__(self, nombre, personalidad, energia, suerte, dinero,
                 frustracion, ego, carisma, confianza, juego_favorito, *ar, **kw):

        self.nombre = nombre
        self.personalidad = personalidad
        self.juego_favorito = juego_favorito

        self._energia = int(energia)
        self._suerte = int(suerte)
        self._dinero = int(dinero)
        self._frustracion = int(frustracion)
        self._ego = int(ego)
        self._carisma = int(carisma)
        self._confianza = int(confianza)

        self.juegos_jugados = []

        # super().__init__(*ar, **kw)

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, value):
        if value < 0:
            self._energia = 0
        elif value > 100:
            self._energia = 100
        else:
            self._energia = value

    @property
    def suerte(self):
        return self._suerte

    @suerte.setter
    def suerte(self, value):
        if value < 0:
            self._suerte = 0
        elif value > 50:
            self._suerte = 50
        else:
            self._suerte = value

    @property
    def dinero(self):
        return self._dinero

    @dinero.setter
    def dinero(self, value):
        if value < 0:
            self._dinero = 0
        else:
            self._dinero = value

    @property
    def frustracion(self):
        return self._frustracion

    @frustracion.setter
    def frustracion(self, value):
        if value < 0:
            self._frustracion = 0
        elif value > 100:
            self._frustracion = 100
        else:
            self._frustracion = value

    @property
    def ego(self):
        return self._ego

    @ego.setter
    def ego(self, value):
        if value < 0:
            self._ego = 0
        elif value > 15:
            self._ego = 15
        else:
            self._ego = value

    @property
    def carisma(self):
        return self._carisma

    @carisma.setter
    def carisma(self, value):
        if value < 0:
            self._carisma = 0
        elif value > 50:
            self._carisma = 50
        else:
            self._carisma = value

    @property
    def confianza(self):
        return self._confianza

    @confianza.setter
    def confianza(self, value):
        if value < 0:
            self._confianza = 0
        elif value > 30:
            self._confianza = 30
        else:
            self._confianza = value

    @abstractmethod
    def comprar_bebestible(self, bebestible, multiplicador: float = 1.0) -> int:
        if self.dinero < bebestible.precio:
            print("\nNo tienes el dinero suficiente para comprar este bebestible!")
            return -1
        else:
            bebestible.consumir(self, multiplicador)
            self.dinero -= bebestible.precio
            return 0

    @abstractmethod
    def apostar(self, juego, apuesta) -> None:
        prob = juego.probabilidad_de_ganar(self, apuesta)

        # print(prob)

        if random.random() <= prob:
            victoria = True
        else:
            victoria = False

        juego.entregar_resultados(self, apuesta, victoria)

        self.juegos_jugados.append(juego.nombre)

    def probabilidad_ganar(self, nombre_juego, apuesta) -> float:
        if nombre_juego == self.juego_favorito:
            es_favorito = 1
        else:
            es_favorito = 0

        probabilidad = min(1, max(0, (self.suerte * 15 - apuesta * 0.4 +
                                      self.confianza * 3 * es_favorito +
                                      self.carisma * 2) / float(1_000)))

        return probabilidad

    def __str__(self):
        descripcion = (f"Nombre: {self.nombre}" +
                       f"\nPersonalidad: {self.personalidad}" +
                       f"\nEnergía: {self.energia}" +
                       f"\nSuerte: {self.suerte}" +
                       f"\nDinero: ${self.dinero:,}" +
                       f"\nFrustración: {self.frustracion}" +
                       f"\nEgo: {self.ego}" +
                       f"\nCarisma: {self.carisma}" +
                       f"\nConfianza: {self.confianza}" +
                       f"\nJuego favorito: {self.juego_favorito}")

        return descripcion


class JugadorLudopata(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        return super().comprar_bebestible(bebestible)

    def apostar(self, juego, apuesta) -> None:
        victoria = None
        super().apostar(juego, apuesta)

        self.ludopatia(victoria)

    def ludopatia(self, victoria) -> None:
        self.ego += parametros.EGO_LUDOPATIA
        self.suerte += parametros.SUERTE_LUDOPATIA

        print(f"Por ser ludópata, el jugador {self.nombre}",
              f"recibe un aumento al ego en {parametros.EGO_LUDOPATIA}",
              f"y a la suerte {parametros.SUERTE_LUDOPATIA} por apostar!")

        if not victoria:
            self.frustracion += parametros.FRUSTRACION_LUDOPATIA
            print("Pero debido a la derrota, su frustración",
                  f"aumenta en {parametros.FRUSTRACION_LUDOPATIA}...")


class JugadorTacano(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        return super().comprar_bebestible(bebestible)

    def apostar(self, juego, apuesta) -> None:
        super().apostar(juego, apuesta)

        self.tacano_extremo(apuesta)

    def tacano_extremo(self, apuesta) -> None:
        if apuesta < (parametros.PORCENTAJE_APUESTA_TACANO * self.dinero):
            bon = parametros.BONIFICACION_TACANO
            self.dinero += bon
            print(
                f"Por ser tacaño, el jugador {self.nombre} recibe ${bon} extra!")


class JugadorBebedor(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        mult = self.cliente_recurrente()
        return super().comprar_bebestible(bebestible, mult)

    def apostar(self, juego, apuesta) -> None:
        return super().apostar(juego, apuesta)

    def cliente_recurrente(self) -> float:
        print("\nPor ser cliente recurrente los bebestibles tienen efectos aumentados...")
        return parametros.MULTIPLICADOR_BONIFICACION_BEBEDOR


class JugadorCasual(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        return super().comprar_bebestible(bebestible)

    def apostar(self, juego, apuesta) -> None:
        self.suerte_principiante()
        super().apostar(juego, apuesta)

    def suerte_principiante(self) -> None:
        if not self.juegos_jugados:
            bon = parametros.BONIFICACION_SUERTE_CASUAL
            print(
                f"\nPor suerte de principiante, el jugador {self.nombre} recibe {bon} de suerte!")
            self.suerte += bon


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
