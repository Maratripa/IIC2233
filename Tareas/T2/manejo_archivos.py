def cargar_puntajes() -> list:
    lista = []
    with open("puntajes.txt", 'r', encoding="utf-8") as file:
        lineas = file.readlines()

        for linea in lineas:
            lista.append(linea.strip('\n').split(','))

    return lista
