import sys
import manejo_csv
import casino


def elegir_jugador():
    # funcion externa que devuelve una lista con jugadores
    jugadores = manejo_csv.obtener_jugadores()

    if not jugadores:
        print("Error leyendo jugadores.csv, lista vacía")
        return

    def print_menu() -> int:
        print(f"\n\n{'*** Opciones de Jugador ***': ^37s}")
        print('-' * 37)

        for i, j in enumerate(jugadores):
            print(f"[{i + 1}] {j.nombre}: {j.personalidad}")

        print("\n[0] Volver")
        print("[X] Salir")

        # Generar tupla con todas las opciones
        opciones = set(range(len(jugadores) + 1)) | {'x'}

        eleccion = funcion(opciones, print_menu)

        if eleccion != None:
            return eleccion
        else:
            sys.exit(2)

    eleccion = print_menu()

    if eleccion in set(range(1, len(jugadores) + 1)):
        return jugadores[eleccion - 1]  # return jugador

    elif eleccion == 0:
        return None

    elif eleccion == -1:  # -1 siempre será eleccion 'x'
        sys.exit(0)

    else:
        # No deberia pasar nunca
        print("Error con función funcion(opciones, elegir_jugador)")
        sys.exit(1)


def funcion(opciones, callback) -> int:
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


def menu_inicio():

    def print_menu() -> int:
        print("\n*** Menú de inicio ***")
        print("----------------------")
        print("[1] Iniciar partida")
        print("[X] Salir")

        opciones = {1, 'x'}  # Tupla con opciones disponibles

        eleccion = funcion(opciones, menu_inicio)

        if eleccion != None:
            return eleccion
        else:
            sys.exit(2)

    eleccion = print_menu()

    if eleccion == 1:
        jugador = elegir_jugador()

        if jugador != None:
            dccasino.jugador = jugador
            dccasino.menu_principal()

        return menu_inicio()

    elif eleccion == -1:  # -1 siempre será eleccion 'x'
        return

    else:
        # No deberia pasar nunca
        print("Error con función funcion(opciones, menu_inicio)")
        return


if __name__ == "__main__":
    print("\n¡BIENVENIDO A DCCASINO!")
    dccasino = casino.Casino()
    menu_inicio()
