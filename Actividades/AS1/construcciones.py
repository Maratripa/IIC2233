from abc import ABC, abstractmethod
from random import choice, randint, random
from unidades import Guerrero, Mago, MagoGuerrero
from parametros import PROB_CRITICO_MURO, PROB_CRITICO_CATAPULTA, \
    HP_MUROCATAPULTA, PROB_CRITICO_MURO_CATAPULTA, \
    HP_BARRACAS, HP_MURO, HP_CATAPULTA


# Recuerda que es una clase abstracta
class Estructura(ABC):

    def __init__(self, edad, *args):
        # No modificar
        super().__init__(*args)
        self.edad = edad
        self.asignar_atributos_segun_edad()

    # ---------------
    # Completar los métodos abstractos aquí
    @abstractmethod
    def asignar_atributos_segun_edad(self):
        pass

    @abstractmethod
    def accion(self):
        pass

    @abstractmethod
    def avanzar_edad(self):
        pass
    # ---------------


# Recuerda completar la herencia
class Barracas(Estructura):

    def __init__(self, *args):
        # Completar
        super().__init__(*args)
        self.hp = HP_BARRACAS

    # ---------------
    # Completar los métodos aquí
    def asignar_atributos_segun_edad(self):
        if self.edad == "Media":
            self.unidades = ["Guerrero", "Mago"]
        elif self.edad == "Moderna":
            self.unidades = ["Guerrero", "Mago", "MagoGuerrero"]

    def avanzar_edad(self):
        if self.edad == "Media":
            self.edad = "Moderna"
            self.unidades.append("MagoGuerrero")
    # ---------------

    def accion(self):
        # No modificar
        elegido = choice(self.unidades)
        suerte = choice((True, False))
        experiencia = choice([1, 2, 3, 4, 5, 6])
        energia = choice([1, 2, 3, 4, 5, 6])
        if elegido == "Guerrero":
            return elegido, Guerrero(suerte, xp=experiencia, stamina=energia)
        elif elegido == "Mago":
            return elegido, Mago(suerte, xp=experiencia, stamina=energia)
        elif elegido == "MagoGuerrero":
            atributos = {"bendito": suerte, "armado": suerte, "xp": experiencia,
                         "stamina": energia}
            return elegido, MagoGuerrero(**atributos)


# Recuerda completar la herencia
class Muro(Estructura):

    def __init__(self, *args):
        # Completar
        super().__init__(*args)
        self.hp = HP_MURO

    # ---------------
    # Completar los métodos aquí
    def asignar_atributos_segun_edad(self):
        if self.edad == "Media":
            self.reparacion = [20, 80]
        elif self.edad == "Moderna":
            self.reparacion = [40, 100]

    def accion(self):
        reconstruccion = randint(*self.reparacion)
        if random() < PROB_CRITICO_MURO:
            return reconstruccion * 2
        else:
            return reconstruccion

    def avanzar_edad(self):
        if self.edad == "Media":
            self.edad = "Moderna"
            self.reparacion = [40, 100]
    # ---------------


# Recuerda completar la herencia
class Catapulta(Estructura):

    def __init__(self, *args):
        # Completar
        super().__init__(*args)
        self.hp = HP_CATAPULTA

    # ---------------
    # Completar los métodos aquí
    def asignar_atributos_segun_edad(self):
        if self.edad == "Media":
            self.ataque = [40, 100]
        elif self.edad == "Moderna":
            self.ataque = [80, 140]

    def accion(self):
        ataque = randint(*self.ataque)
        if random() < PROB_CRITICO_CATAPULTA:
            return ataque * 2
        else:
            return ataque

    def avanzar_edad(self):
        if self.edad == "Media":
            self.edad = "Moderna"
            self.ataque = [80, 140]
    # ---------------


# Recuerda completar la herencia
class MuroCatapulta(Muro, Catapulta):

    def __init__(self, *args):
        # Completar
        super().__init__(*args)
        self.hp = HP_MUROCATAPULTA

    # ---------------
    # Completar los métodos aquí
    def asignar_atributos_segun_edad(self):
        Muro.asignar_atributos_segun_edad(self)
        Catapulta.asignar_atributos_segun_edad(self)

    def accion(self):
        reparacion = randint(*self.reparacion)
        ataque = randint(*self.ataque)

        if random() < PROB_CRITICO_MURO_CATAPULTA:
            return (round(reparacion * 5 / 2), round(ataque * 5 / 2))
        else:
            return (reparacion, ataque)

    def avanzar_edad(self):
        if self.edad == "Media":
            self.edad = "Moderna"
            self.reparacion = [40, 100]
            self.ataque = [80, 140]
    # ---------------


if __name__ == "__main__":
    # ---------------
    # En esta sección puedes probar tu codigo
    # ---------------
    mc = MuroCatapulta("Moderna")

    print(mc.accion())
    print(mc.edad)
    print(mc.reparacion)
    print(mc.ataque)
    mc.avanzar_edad()
    print(mc.edad)
    print(mc.reparacion)
    print(mc.ataque)
