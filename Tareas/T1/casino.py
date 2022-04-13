import sys
import random

import parametros
import manejo_csv


# Funcion para validar input y llamar a una funcion de callback en caso de que la opcion elegida
# no este dentro de las opciones
def funcion(opciones: set, callback) -> int:
    eleccion = input("\nIngrese opción: ")

    if eleccion.isnumeric():
        # revisar si el numero esta en las opciones
        if int(eleccion) in opciones:
            return int(eleccion)

        else:
            return callback()

    else:
        if eleccion in opciones:  # 'x'
            return -1

        else:
            return callback()


class Casino:

    def __init__(self):
        self.jugador = None  # se setea despues de __init__ y se puede cambiar en el menu inicial
        self.bebestibles = []  # lista de Bebestibles
        self.juegos = []  # lista de Juegos
        self.dinero_faltante = parametros.DEUDA_TOTAL

        self.opcion_pagar = False  # boolean para pagar deuda en caso que se pueda

        self.cargar_contenido()

    def cargar_contenido(self) -> None:
        # devuelve una lista con los bebestibles disponibles
        self.bebestibles = manejo_csv.obtener_bebestibles()

        # devuelve una lista con los juegos disponibles
        self.juegos = manejo_csv.obtener_juegos()

        return

    def evento_especial(self) -> None:
        if random.random() < parametros.PROBABILIDAD_EVENTO:
            print(f"\n{'** EVENTO ESPECIAL **': ^37}\n")

            beb = random.choice(self.bebestibles)  # bebestible aleatorio

            print(
                f"Al jugador {self.jugador.nombre} le han regalado un {beb.nombre}")

            # activar la abilidad de JugadorBebedor si este lo es
            if self.jugador.personalidad == "Bebedor":
                mult = self.jugador.cliente_recurrente()
                beb.consumir(self.jugador, mult)

            else:  # consumir sin multiplicador para el resto de los jugadores
                beb.consumir(self.jugador)

    def jugar(self, juego) -> str:
        if self.jugador.agotado:
            m = (f"\nEl jugador {self.jugador.nombre}",
                 "no tiene la energía suficiente para seguir jugando...")

            return m  # mensaje de error

        if self.jugador.dinero >= juego.apuesta_minima:
            juego.menu_de_juego(self.jugador)  # ir al menu del juego

            return ""  # no hay errores

        else:
            m = (f"\nEl jugador {self.jugador.nombre} no tiene dinero" +
                 f" suficiente para jugar {juego.nombre}")

            return m  # mensaje de error

    def menu_principal(self, mensaje_error=""):
        # volver al menu de inicio si el jugador queda en quiebra
        if self.jugador.quiebra:
            print(
                "\n\nTe quedaste sin dinero y BigCat ha mandado a sus matones a por ti...")
            return

        # resetear la opcion de pagar si el jugador pierde dinero
        if self.jugador.dinero < self.dinero_faltante:
            self.opcion_pagar = False

        # Dar la opcion de pagar deuda si se acaba de llegar a la cantidad de dinero
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

            if accion == 0:  # terminar juego
                print(f"\n\n{'*** FELICIDADES ***': ^37}\n")
                print("Has logrado saldar tu deuda con BigCat y eres libre!\n")
                sys.exit(0)

            elif accion == 1:  # seguir jugando
                self.opcion_pagar = True

        # imprimir menu y validar input
        def print_menu(m="") -> int:
            print(f"\n\n{'*** Menú principal ***': ^37s}\n")
            print(
                f"Jugador: {self.jugador.nombre} - {self.jugador.personalidad}")
            print('-' * 37)
            print("[1] Opciones de juegos")
            print("[2] Comprar bebestible")
            print("[3] Estado jugador")
            print("[4] Show")

            # añadir opcion de pagar deuda al menu
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
            return self.menu_juegos()  # menu del los juegos

        elif accion == 2:
            return self.menu_bebestibles()  # menu de los bebestibles

        elif accion == 3:
            return self.estado_jugador()  # mostrar estado del jugador

        elif accion == 4:
            return self.show()  # comprar entrada al show

        elif accion == 5 and self.opcion_pagar:  # pagar la deuda y salir del juego
            print(f"\n\n{'*** FELICIDADES ***': ^37}\n")
            print("Has logrado saldar tu deuda con BigCat y eres libre!\n")
            sys.exit(0)

        elif accion == 0:  # volver al menu de inicio y resetear la opcion de pagar
            self.opcion_pagar = False
            return

        elif accion == -1:  # salir
            sys.exit(0)

    def menu_bebestibles(self):

        def print_menu() -> int:
            print(f"\n\n{'*** Bebestibles ***': ^37s}\n")
            print(
                f"{'N°': ^4s} | {'Nombre': <14s} | {'Tipo': <14s} | {'Precio': ^5s}")
            print('~' * 47)

            # imprimir todos los bebestibles
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

        if accion in set(range(1, len(self.bebestibles) + 1)):
            # intentar comprar bebestible
            respuesta = self.jugador.comprar_bebestible(
                self.bebestibles[accion - 1])

            if respuesta == -1:  # no tiene dinero suficiente para comprar el bebestible
                return self.menu_bebestibles()

            elif respuesta == 0:  # compra exitosa
                return self.menu_principal()

        elif accion == 0:
            return self.menu_principal()

        elif accion == -1:
            sys.exit(0)

    def menu_juegos(self):

        # imprimir menu y validar input
        def print_menu() -> int:
            print(f"\n\n{'*** Opciones de Juegos ***': ^37s}")
            print('-' * 37)

            # imprimir todos los juegos
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
            self.evento_especial()  # despues de cada apuesta ver si se activa el evento
            return self.menu_principal(m)  # volver al menu principal

        elif accion == 0:
            return self.menu_principal()  # volver

        elif accion == -1:
            sys.exit(0)  # salir

    def estado_jugador(self):

        def print_menu() -> int:
            print(f"\n\n{'*** Ver estado del Jugador ***': ^45s}")
            print('-' * 45)
            print(self.jugador)
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
            return self.menu_principal()  # volver

        elif accion == -1:
            sys.exit(0)  # salir

    def show(self):
        # algunos tipos de show :)
        shows = ["circo", "concierto", "teatro", "premiere de cine"]

        if self.jugador.dinero < parametros.DINERO_SHOW:
            print("No tienes suficiente dinero para ver el show...")
            return self.menu_principal()  # no le han pagado la ayudantia

        # ver show :D
        else:
            self.jugador.dinero -= parametros.DINERO_SHOW
            self.jugador.energia += parametros.ENERGIA_SHOW
            self.jugador.frustracion += parametros.FRUSTRACION_SHOW

            print(f"\nEl jugador {self.jugador.nombre} ha pagado {parametros.DINERO_SHOW}",
                  f"para ver el show de {random.choice(shows)}.")
            print(f"Gracias a esto, ha recuperado {parametros.ENERGIA_SHOW} de energía",
                  f"y ha disminuído en {parametros.FRUSTRACION_SHOW} su frustración.\n")

            return self.menu_principal()
