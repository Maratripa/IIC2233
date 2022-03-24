from parametros import PROBABILIDAD_EVENTO, PUBLICO_EXITO, PUBLICO_INICIAL, \
    PUBLICO_TERREMOTO, AFINIDAD_OLA_CALOR, \
    AFINIDAD_LLUVIA, PUBLICO_OLA_CALOR
from random import random, choice


class DCConcierto:

    def __init__(self):
        self.artista_actual = ''
        self.__dia = 1
        self.line_up = []
        self.cant_publico = PUBLICO_INICIAL
        self.artistas = []
        self.prob_evento = PROBABILIDAD_EVENTO
        self.suministros = []

    @property
    def dia(self):
        return self.__dia

    @dia.setter
    def dia(self, value):
        if value < 1:
            self.__dia = 1

        if value > self.dia:
            self.__dia = value

    @property
    def funcionando(self):
        return self.exito_del_concierto and self.dia <= 3

    @property
    def exito_del_concierto(self):
        return self.cant_publico >= PUBLICO_EXITO

    def imprimir_estado(self):
        print(f"Día: {self.__dia}\nCantidad de Personas: "
              f"{self.cant_publico}\nArtistas:")
        for artista in self.line_up:
            print(f"- {artista.nombre}")

    def ingresar_artista(self, artista):
        self.line_up.append(artista)
        print(f'Se ha ingresado un nuevo artista!!!\n{artista}')

    def asignar_lineup(self):
        self.line_up = []
        for artista in self.artistas:
            if self.dia == artista.dia_presentacion:
                self.ingresar_artista(artista)

    def nuevo_dia(self):
        self.dia += 1

        if self.funcionando:
            print("Comienza un nuevo dia!")

    def ejecutar_evento(self):
        if random() <= self.prob_evento:
            evento = choice(("Lluvia", "Terremoto", "Calor"))
            actual = self.artista_actual

            if evento == "Lluvia":
                self.artista_actual.afinidad_con_publico -= AFINIDAD_LLUVIA
                print(
                    "Debido a la lluvia, la afinidad con el publico de",
                    f"{actual.nombre} ha disminuido en {AFINIDAD_LLUVIA}")

            elif evento == "Terremoto":
                self.cant_publico -= PUBLICO_TERREMOTO
                print(
                    "Debido al terremoto,",
                    f"la cantidad de publico ha disminuido en {PUBLICO_TERREMOTO}")

            elif evento == "Calor":
                self.artista_actual.afinidad_con_publico -= AFINIDAD_OLA_CALOR
                self.cant_publico -= PUBLICO_OLA_CALOR
                print(
                    f"Debido a la ola de calor, la afinidad con el publico de {actual.nombre}",
                    f"ha disminuido en {AFINIDAD_OLA_CALOR}, Ademas, {PUBLICO_OLA_CALOR}",
                    "personas se han ido del concierto.")
