def cargar_puntajes() -> list:
    lista = []
    with open("puntajes.txt", 'r', encoding="utf-8") as file:
        lineas = file.readlines()

        for linea in lineas:
            if linea.strip():
                lista.append(linea.strip('\n').split(','))

    lista.sort(key=lambda ls: int(ls[1]), reverse=True)

    return lista


def guardar_puntaje(usuario, puntaje) -> None:
    tiene_n = False
    with open("puntajes.txt", 'r', encoding="utf-8") as file:
        archivo_completo = file.read()
        if archivo_completo.endswith('\n'):
            tiene_n = True
    with open("puntajes.txt", 'a', encoding="utf-8") as file:
        if tiene_n:
            linea = f"{usuario},{puntaje}\n"
        else:
            linea = f"\n{usuario},{puntaje}\n"

        print(linea, file=file)
