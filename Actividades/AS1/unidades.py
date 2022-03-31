from abc import ABC, abstractmethod
from parametros import PROB_REVIVIR, PROB_CRITICO_GUERRERO, \
    PROB_CRITICO_MAGO, PROB_CRITICO_MAGO_GUERRERO
import math
import random


# Recuerda que es una clase abstracta
class Persona(ABC):

    def __init__(self, xp, stamina, **kwargs):
        # No modificar
        super().__init__(**kwargs)
        self.xp = xp
        self.stamina = stamina
        self.asignar_parametros()

    @property
    def stamina(self):
        # No modificar
        return self._stamina

    @stamina.setter
    def stamina(self, value):
        # No modificar
        if value <= 0:
            if not self.revivir():
                print("F")
        else:
            self._stamina = value

    def revivir(self):
        # No modificar
        if PROB_REVIVIR > random.random():
            self.stamina += 3
            return True
        else:
            return False

    # ---------------
    # Completar los métodos abstractos aquí
    @abstractmethod
    def asignar_parametros(self):
        pass

    @abstractmethod
    def accion(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
    # ---------------


# Recuerda completar la herencia
class Guerrero(Persona):

    def __init__(self, armado, **kwargs):
        # Completar
        self.armado = armado
        super().__init__(**kwargs)

    # ---------------
    # Completar los métodos aquí
    def asignar_parametros(self):
        ataque = round(5 * math.pi * self.xp / 2)
        if self.armado:
            self.ataque = ataque * 2
        else:
            self.ataque = ataque

    def accion(self):
        if random.random() < PROB_CRITICO_GUERRERO:
            return round(self.ataque * 3 / 2)
        else:
            return self.ataque

    def __str__(self):
        string = None
        if self.armado:
            string = f"Guerrero Armado con {self.ataque} pts de ataque"
        else:
            string = f"Guerrero con {self.ataque} pts de ataque"

        return string
    # ---------------


# Recuerda completar la herencia
class Mago(Persona):

    def __init__(self, bendito, **kwargs):
        # Completar
        self.bendito = bendito
        super().__init__(**kwargs)

    # ---------------
    # Completar los métodos aquí
    def asignar_parametros(self):
        curacion = round(1.6180 * math.pi * self.xp / 2)

        if self.bendito:
            self.curacion = curacion * 2
        else:
            self.curacion = curacion

    def accion(self):
        if random.random() < PROB_CRITICO_MAGO:
            return round(self.curacion * 3 / 2)
        else:
            return self.curacion

    def __str__(self):
        if self.bendito:
            return f"Mago BENDITO con {self.curacion} pts de curación"
        else:
            return f"Mago con {self.curacion} pts de curación"
    # ---------------


# Recuerda completar la herencia
class MagoGuerrero(Mago, Guerrero):

    def __init__(self, **kwargs):
        # Completar
        super().__init__(**kwargs)

    # ---------------
    # Completar los métodos aquí
    def asignar_parametros(self):
        Mago.asignar_parametros(self)
        Guerrero.asignar_parametros(self)

    def accion(self):
        if random.random() < PROB_CRITICO_MAGO_GUERRERO:
            return (self.ataque * 2, self.curacion * 2)
        else:
            return (self.ataque, self.curacion)
    # ---------------

    def __str__(self):
        # No modificar
        if self.armado and self.bendito:
            return f"MagoGuerrero BENDITO y ARMADO con {self.curacion}" \
                   + f" pts de curación y {self.ataque} pts de ataque."
        else:
            return f"MagoGuerrero con {self.curacion} pts de curación" \
                + f" y {self.ataque} pts de ataque."


if __name__ == "__main__":
    # ---------------
    # En esta sección puedes probar tu codigo
    # ---------------
    magoguerrero = MagoGuerrero(bendito=True, armado=False, xp=100, stamina=5)
    print(magoguerrero)
