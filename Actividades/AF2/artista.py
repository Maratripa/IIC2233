from parametros import (AFINIDAD_HIT, AFINIDAD_INICIAL, AFINIDAD_PUBLICO_POP,
                        AFINIDAD_STAFF_POP, AFINIDAD_PUBLICO_ROCK,
                        AFINIDAD_STAFF_ROCK, AFINIDAD_PUBLICO_RAP,
                        AFINIDAD_STAFF_RAP, AFINIDAD_PUBLICO_REG,
                        AFINIDAD_STAFF_REG, AFINIDAD_ACCION_POP,
                        AFINIDAD_ACCION_ROCK, AFINIDAD_ACCION_RAP,
                        AFINIDAD_ACCION_REG, AFINIDAD_MIN, AFINIDAD_MAX)


class Artista:
    def __init__(self, nombre, genero, dia_presentacion,
                 hit_del_momento):
        self.nombre = nombre
        self.hit_del_momento = hit_del_momento
        self.genero = genero
        self.dia_presentacion = dia_presentacion
        self._afinidad_con_publico = AFINIDAD_INICIAL
        self._afinidad_con_staff = AFINIDAD_INICIAL

    @property
    def afinidad_con_publico(self):
        return self._afinidad_con_publico

    @afinidad_con_publico.setter
    def afinidad_con_publico(self, value):
        if value > 100:
            self._afinidad_con_publico = 100
        elif value < 0:
            self._afinidad_con_publico = 0
        else:
            self._afinidad_con_publico = value

    @property
    def afinidad_con_staff(self):
        return self._afinidad_con_staff

    @afinidad_con_staff.setter
    def afinidad_con_staff(self, value):
        if value > 100:
            self._afinidad_con_staff = 100
        elif value < 0:
            self._afinidad_con_staff = 0
        else:
            self._afinidad_con_staff = value

    @property
    def animo(self):
        animo = (self.afinidad_con_publico / 2) + (self.afinidad_con_staff / 2)
        return animo

    def recibir_suministros(self, suministro):
        valor = suministro.valor_de_satisfaccion

        self.afinidad_con_staff += valor

        if valor < 0:
            print(f"{self.nombre} recibió {suministro.nombre} en malas condiciones.")
        else:
            print(f"{self.nombre} recibió un {suministro.nombre} a tiempo!")

    def cantar_hit(self):
        self.afinidad_con_publico += AFINIDAD_HIT

        print(f"{self.nombre} está tocando su hit: {self.hit_del_momento}!")

    def __str__(self):
        string = (f"Nombre: {self.nombre}\n" +
                  f"Genero: {self.genero}\n" +
                  f"Animo: {self.animo}")

        return string


class ArtistaPop(Artista):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.accion = "Cambio de vestuario"
        self._afinidad_con_publico = AFINIDAD_PUBLICO_POP
        self._afinidad_con_staff = AFINIDAD_STAFF_POP

    def accion_especial(self):
        self.afinidad_con_publico += AFINIDAD_ACCION_POP

        print(f"{self.nombre} hará un {self.accion}")

    @property
    def animo(self):
        if super().animo < 10:
            print(
                f"ArtistaPop peligrando en el concierto. Animo: {super().animo}")

        return super().animo


class ArtistaRock(Artista):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.accion = "Solo de guitarra"
        self._afinidad_con_publico = AFINIDAD_PUBLICO_ROCK
        self._afinidad_con_staff = AFINIDAD_STAFF_ROCK

    def accion_especial(self):
        self.afinidad_con_publico += AFINIDAD_ACCION_ROCK

        print(f"{self.nombre} hará un {self.accion}")

    @property
    def animo(self):
        if super().animo < 5:
            print(
                f"ArtistaRock peligrando en el concierto. Animo: {self.animo}")

        return super().animo


class ArtistaRap(Artista):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.accion = "Doble tempo"
        self._afinidad_con_publico = AFINIDAD_PUBLICO_RAP
        self._afinidad_con_staff = AFINIDAD_STAFF_RAP

    def accion_especial(self):
        self.afinidad_con_publico += AFINIDAD_ACCION_RAP

        print(f"{self.nombre} hará un {self.accion}")

    @property
    def animo(self):
        if super().animo < 20:
            print(
                f"ArtistaRap peligrando en el concierto. Animo: {self.animo}")

        return super().animo


class ArtistaReggaeton(Artista):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.accion = "Perrear"
        self._afinidad_con_publico = AFINIDAD_PUBLICO_REG
        self._afinidad_con_staff = AFINIDAD_STAFF_REG

    def accion_especial(self):
        self.afinidad_con_publico += AFINIDAD_ACCION_REG

        print(f"{self.nombre} hará un {self.accion}")

    @property
    def animo(self):
        if super().animo < 2:
            print(
                f"ArtistaReggaeton peligrando en el concierto. Animo: {self.animo}")

        return super().animo
