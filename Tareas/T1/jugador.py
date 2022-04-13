from abc import ABC, abstractmethod
import random

import parametros


class Jugador(ABC):

    def __init__(self, nombre, personalidad, energia, suerte, dinero,
                 frustracion, ego, carisma, confianza, juego_favorito, *ar, **kw):

        self.nombre = nombre  # str
        self.personalidad = personalidad  # str
        self.juego_favorito = juego_favorito  # str

        """
        INICIO PROPERTIES
        """
        self._energia = int(energia)
        self._suerte = int(suerte)
        self._dinero = int(dinero)
        self._frustracion = int(frustracion)
        self._ego = int(ego)
        self._carisma = int(carisma)
        self._confianza = int(confianza)
        """
        FIN PROPERTIES
        """

        self.juegos_jugados = []

        self.quiebra = False  # para ver si eliminar al jugador de la lista
        self.agotado = False  # para ver si puede apostar o no

    """
    Cada property esta definida con sus setters para establecer limites
    """

    @property
    def energia(self):
        return self._energia

    @energia.setter
    def energia(self, value):
        if value < 0:
            self._energia = 0
            self.agotado = True

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
        if value <= 0:
            self._dinero = 0
            self.quiebra = True

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

    # metodo de clase que deben implementar en cada subclase
    @abstractmethod
    def comprar_bebestible(self, bebestible, multiplicador: float = 1.0) -> int:
        if self.dinero < bebestible.precio:
            print("\nNo tienes el dinero suficiente para comprar este bebestible!")
            return -1

        else:
            # multiplicador del borracho
            bebestible.consumir(self, multiplicador)
            self.dinero -= bebestible.precio
            return 0

    # metodo que se debe reimplementar
    @abstractmethod
    def apostar(self, juego, apuesta) -> None:
        prob = juego.probabilidad_de_ganar(self, apuesta)  # float

        if random.random() <= prob:
            victoria = True  # gano :)

        else:
            victoria = False  # perdio :(

        # imprimir resultados y cambiar atributos del jugador
        juego.entregar_resultados(self, apuesta, victoria)

        self.energia -= round((self.ego + self.frustracion)
                              * 0.15)  # quitar energia

        # añadir juego a la lista de jugados
        self.juegos_jugados.append(juego.nombre)

    def probabilidad_ganar(self, nombre_juego, apuesta) -> float:
        # aplicar bonus si es juego favorito
        if nombre_juego == self.juego_favorito:
            es_favorito = 1

        else:
            es_favorito = 0

        # se añade el max() para que no hayan probabilidades negativas
        probabilidad = min(1, max(0, (self.suerte * 15 - apuesta * 0.4 +
                                      self.confianza * 3 * es_favorito +
                                      self.carisma * 2) / float(1_000)))

        return probabilidad

    # facilita imprimir estado del jugador
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
        return super().comprar_bebestible(bebestible)  # no hay cambios en el metodo

    def apostar(self, juego, apuesta) -> None:
        victoria = None
        super().apostar(juego, apuesta)

        # habilidad del jugador se activa depues de la apuesta
        self.ludopatia(victoria)

    def ludopatia(self, victoria) -> None:  # habilidad
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
        return super().comprar_bebestible(bebestible)  # no se modifica el metodo

    def apostar(self, juego, apuesta) -> None:
        victoria = None
        super().apostar(juego, apuesta)

        if victoria:
            # metodo se activa despues de apostar solo si gana
            self.tacano_extremo(apuesta)

    def tacano_extremo(self, apuesta) -> None:  # habilidad
        if apuesta < (parametros.PORCENTAJE_APUESTA_TACANO * self.dinero):
            bon = parametros.BONIFICACION_TACANO
            self.dinero += bon
            print(
                f"Por ser tacaño, el jugador {self.nombre} recibe ${bon} extra!")


class JugadorBebedor(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        mult = self.cliente_recurrente()  # se calcula el multiplicador
        return super().comprar_bebestible(bebestible, mult)

    def apostar(self, juego, apuesta) -> None:
        return super().apostar(juego, apuesta)  # no se modifica el metodo

    def cliente_recurrente(self) -> float:  # habilidad
        print("\nPor ser cliente recurrente los bebestibles tienen efectos aumentados...")
        return parametros.MULTIPLICADOR_BONIFICACION_BEBEDOR


class JugadorCasual(Jugador):

    def __init__(self, *ar, **kw):
        super().__init__(*ar, **kw)

    def comprar_bebestible(self, bebestible) -> int:
        return super().comprar_bebestible(bebestible)  # no se modifica el metodo

    def apostar(self, juego, apuesta) -> None:
        self.suerte_principiante()  # habilidad antes de apostar
        super().apostar(juego, apuesta)

    def suerte_principiante(self) -> None:
        if not self.juegos_jugados:
            bon = parametros.BONIFICACION_SUERTE_CASUAL
            print(
                f"\nPor suerte de principiante, el jugador {self.nombre} recibe {bon} de suerte!")
            self.suerte += bon
