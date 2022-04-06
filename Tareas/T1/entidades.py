from abc import ABC, abstractmethod
import parametros
import random


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
    def comprar_bebestible(self, bebestible):
        pass

    @abstractmethod
    def apostar(self, juego):
        pass

    def probabilidad_ganar(self, nombre_juego, apuesta):
        es_favorito = nombre_juego == self.juego_favorito

        probabilidad = min(1, max(0, (self.suerte * 15 - apuesta * 0.4 +
                                      self.confianza * 3 * es_favorito + self.carisma * 2) / 1_000))

        return probabilidad

    def __str__(self):
        descripcion = (f"Nombre: {self.nombre}" +
                       f"\nPersonalidad: {self.personalidad}" +
                       f"\nEnergía: {self.energia}" +
                       f"\nSuerte: {self.suerte}" +
                       f"\nDinero: {self.dinero}" +
                       f"\nFrustración: {self.frustracion}" +
                       f"\nEgo: {self.ego}" +
                       f"\nCarisma: {self.carisma}" +
                       f"\nConfianza: {self.confianza}" +
                       f"\nJuego favorito: {self.juego_favorito}")

        return descripcion


class JugadorLudopata(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible):
        return super().comprar_bebestible(bebestible)

    def apostar(self):
        return super().apostar()


class JugadorTacano(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible):
        return super().comprar_bebestible(bebestible)

    def apostar(self):
        return super().apostar()


class JugadorBebedor(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible):
        return super().comprar_bebestible(bebestible)

    def apostar(self):
        return super().apostar()


class JugadorCasual(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible):
        return super().comprar_bebestible(bebestible)

    def apostar(self):
        return super().apostar()


class Juego:

    def __init__(self, nombre, esperanza, ap_min, ap_max, *ar, **kw):
        self.nombre = nombre
        self.esperanza = int(esperanza)
        self.apuesta_minima = int(ap_min)
        self.apuesta_maxima = int(ap_max)

    def entregar_resultados(self):
        pass

    def probabilidad_de_ganar(self, jugador):
        pass

    def es_favorito(self, jugador):
        pass

    def menu_de_juego(self):

        def print_menu() -> int:
            titulo = f"*** {self.nombre} ***"
            print(f"{titulo: ^37s}")
            print('-' * 37)

        accion = print_menu()


class Bebestible(ABC):

    def __init__(self, nombre, tipo, precio, *ar, **kw):
        self.nombre = nombre
        self.tipo = tipo
        self.precio = int(precio)

    @abstractmethod
    def consumir(self, jugador: Jugador):
        recuperacion = random.randint(
            parametros.MIN_ENERGIA_BEBESTIBLE, parametros.MAX_ENERGIA_BEBESTIBLE)

        jugador.energia += recuperacion
        print(
            f"El jugador {jugador.nombre} ha recuperado {recuperacion} energía!")


class Jugo(Bebestible):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador):
        super().consumir(jugador)

        if len(self.nombre) <= 4:
            jugador.ego += 4
            print(f"El ego del jugador {jugador.nombre} ha aumentado en 4!")

        elif 5 <= len(self.nombre) <= 7:
            jugador.suerte += 7
            print(f"La suerte del jugador {jugador.nombre} ha aumentado en 7!")

        elif 8 <= len(self.nombre):
            jugador.frustracion -= 10
            jugador.ego += 11
            print(f"La frustración del jugador {jugador.nombre} ha disminuído en 10,",
                  "pero el ego ha aumentado en 11!")


class Gaseosa(Bebestible):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador):
        super().consumir(jugador)

        if isinstance(jugador, JugadorTacano) or isinstance(jugador, JugadorLudopata):
            jugador.frustracion -= 5
            print(
                f"La frustración del jugador {jugador.nombre} ha disminuído en 5!")

        elif isinstance(jugador, JugadorBebedor) or isinstance(jugador, JugadorCasual):
            jugador.frustracion += 5
            print(
                f"La frustración del jugador {jugador.nombre} ha aumentado en 5!")

        jugador.ego += 6
        print(f"El ego del jugador {jugador.nombre} ha aumentado en 6!")


class BrebajeMagico(Jugo, Gaseosa):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def consumir(self, jugador: Jugador):
        Jugo.consumir(self, jugador)
        Gaseosa.consumir(self, jugador)

        jugador.carisma += 5
        print(f"El carisma del jugador {jugador.nombre} ha aumento en 5!")
