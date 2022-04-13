import sys
import random

import parametros
import manejo_csv


def funcion(opciones: set, callback) -> int:
    eleccion = input("\nIngrese opción: ")

    if eleccion.isnumeric():
        if int(eleccion) in opciones:
            return int(eleccion)

        else:
            return callback()

    else:
        if eleccion in opciones:
            return -1

        else:
            return callback()


class Casino:

    def __init__(self):
        self.jugador = None
        self.bebestibles = []
        self.juegos = []
        self.dinero_faltante = parametros.DEUDA_TOTAL

        self.opcion_pagar = False

        self.cargar_contenido()

    def cargar_contenido(self) -> None:
        self.bebestibles = manejo_csv.obtener_bebestibles()
        self.juegos = manejo_csv.obtener_juegos()

        return

    def evento_especial(self) -> None:
        if random.random() < parametros.PROBABILIDAD_EVENTO:
            print(f"\n{'** EVENTO ESPECIAL **': ^37}\n")
            beb = random.choice(self.bebestibles)
            print(
                f"Al jugador {self.jugador.nombre} le han regalado un {beb.nombre}")

            if self.jugador.personalidad == "Bebedor":
                mult = self.jugador.cliente_recurrente()
                beb.consumir(self.jugador, mult)
            else:
                beb.consumir(self.jugador)

    def jugar(self, juego) -> str:
        if self.jugador.dinero >= juego.apuesta_minima:
            juego.menu_de_juego(self.jugador)
            return ""
        else:
            m = (f"\nEl jugador {self.jugador.nombre} no tiene dinero" +
                 f" suficiente para jugar {juego.nombre}")

            return m

    def menu_principal(self, mensaje_error=""):

        if self.jugador.dinero >= self.dinero_faltante and not self.opcion_pagar:
            def print_menu() -> int:
                print("\n\nTienes suficiente dinero como para")
                print("pagar toda tu deuda. ¿Deseas saldar cuentas")
                print("y salir o seguir jugando?")

                print("\n[0] Saldar deuda")
                print("[1] Seguir jugando")

                opciones = {0, 1}

                eleccion = funcion(opciones, print_menu)

                if eleccion != None:
                    return eleccion
                else:
                    sys.exit(2)

            accion = print_menu()

            if accion == 0:
                print(f"\n\n{'*** FELICIDADES ***': ^37}\n")
                print("Has logrado saldar tu deuda con BigCat y eres libre!\n")
                sys.exit(0)
            elif accion == 1:
                self.opcion_pagar = True

        def print_menu(m="") -> int:
            print(f"\n\n{'*** Menú principal ***': ^37s}\n")
            print(
                f"Jugador: {self.jugador.nombre} - {self.jugador.personalidad}")
            print('-' * 37)
            print("[1] Opciones de juegos")
            print("[2] Comprar bebestible")
            print("[3] Estado jugador")
            print("[4] Show")  # TODO

            if self.opcion_pagar:
                print("[5] Pagar deuda")
                opciones = set(range(6)) | {'x'}
            else:
                opciones = set(range(5)) | {'x'}

            print(m)
            print("[0] Volver")
            print("[X] Salir")

            eleccion = funcion(opciones, print_menu)

            if eleccion != None:
                return eleccion
            else:
                sys.exit(2)

        accion = print_menu(mensaje_error)

        if accion == 1:
            return self.menu_juegos()

        elif accion == 2:
            return self.menu_bebestibles()

        elif accion == 3:
            return self.estado_jugador()

        elif accion == 4:
            return self.show()

        elif accion == 5 and self.opcion_pagar:
            print(f"\n\n{'*** FELICIDADES ***': ^37}\n")
            print("Has logrado saldar tu deuda con BigCat y eres libre!\n")
            sys.exit(0)

        elif accion == 0:
            self.opcion_pagar = False
            return

        elif accion == -1:
            sys.exit(0)

    def menu_bebestibles(self):

        def print_menu() -> int:
            print(f"\n\n{'*** Bebestibles ***': ^37s}\n")
            print(
                f"{'N°': ^4s} | {'Nombre': <14s} | {'Tipo': <14s} | {'Precio': ^5s}")
            print('~' * 47)

            for i, b in enumerate(self.bebestibles):
                number_str = f'[{i + 1}]'
                print(
                    f"{number_str: ^4.4s} | {b.nombre: <14.14s} | {b.tipo: <14.14s} | ${b.precio: ^4}")

            print("\n[0] Volver")
            print("[X] Salir")

            opciones = set(range(len(self.bebestibles) + 1)) | {'x'}

            eleccion = funcion(opciones, print_menu)

            if eleccion != None:
                return eleccion
            else:
                sys.exit(2)

        accion = print_menu()

        # print(f"accion: {accion}")

        if accion in set(range(1, len(self.bebestibles) + 1)):
            respuesta = self.jugador.comprar_bebestible(
                self.bebestibles[accion - 1])

            if respuesta == -1:
                return self.menu_bebestibles()
            elif respuesta == 0:
                return self.menu_principal()

        elif accion == 0:
            return self.menu_principal()

        elif accion == -1:
            sys.exit(0)

    def menu_juegos(self):

        def print_menu() -> int:
            print(f"\n\n{'*** Opciones de Juegos ***': ^37s}")
            print('-' * 37)

            for i, j in enumerate(self.juegos):
                print(f"[{i + 1}] {j.nombre}")

            print("\n[0] Volver")
            print("[X] Salir")

            opciones = set(range(len(self.juegos) + 1)) | {'x'}

            eleccion = funcion(opciones, print_menu)

            if eleccion != None:
                return eleccion
            else:
                sys.exit(2)

        accion = print_menu()

        if accion in set(range(1, len(self.juegos) + 1)):
            m = self.jugar(self.juegos[accion - 1])
            self.evento_especial()
            return self.menu_principal(m)

        elif accion == 0:
            return self.menu_principal()

        elif accion == -1:
            sys.exit(0)

    def estado_jugador(self):
        j = self.jugador

        def print_menu() -> int:
            print(f"\n\n{'*** Ver estado del Jugador ***': ^45s}")
            print('-' * 45)
            print(j)
            print(f"Dinero faltante: ${self.dinero_faltante:,}")
            print("\n[0] Volver")
            print("[X] Salir")

            opciones = {0, 'x'}

            eleccion = funcion(opciones, print_menu)

            if eleccion != None:
                return eleccion
            else:
                sys.exit(2)

        accion = print_menu()

        if accion == 0:
            return self.menu_principal()

        elif accion == -1:
            sys.exit(0)

    def show(self):
        shows = ["circo", "concierto", "teatro", "premiere de cine"]

        if self.jugador.dinero < parametros.DINERO_SHOW:
            print("No tienes suficiente dinero para ver el show...")
            return self.menu_principal()
        else:
            self.jugador.dinero -= parametros.DINERO_SHOW
            self.jugador.energia += parametros.ENERGIA_SHOW
            self.jugador.frustracion += parametros.FRUSTRACION_SHOW

            print(f"\nEl jugador {self.jugador.nombre} ha pagado {parametros.DINERO_SHOW}",
                  f"para ver el show de {random.choice(shows)}.")
            print(f"Gracias a esto, ha recuperado {parametros.ENERGIA_SHOW} de energía",
                  f"y ha disminuído en {parametros.FRUSTRACION_SHOW} su frustración.\n")

            return self.menu_principal()
