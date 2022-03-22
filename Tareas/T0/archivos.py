import os
from entidades.usuario import UsuarioRegistrado
from entidades.encomienda import Encomienda
from entidades.reclamo import Reclamo


# Buscar usuario en csv/usuarios.csv
def buscar_usuario(username: str, password: str):
    #
    # Retornar None, 1 en caso de no encontrar un usuario con el username dado
    # Retornar None, 2 en caso de que la contraseña sea incorrecta
    #

    users_dict = {}

    with open(os.path.join("csv", "usuarios.csv"), 'r', encoding="utf-8") as file:
        users = file.readlines()

        for user in users[1:]:
            u = user.strip().split(',')
            users_dict[u[0]] = u[1]

    if username not in users_dict:
        return None, 1

    if password != users_dict[username]:
        return None, 2

    return UsuarioRegistrado(username, password), 0


# Agregar usuario nuevo a csv/usuarios.csv
def registrar_usuario(username: str, password: str):
    #
    # Verificar datos y retornar None, 1 si ya hay un usuario con el username dado
    # Retornar None, 2 si el usuario no cumple con los requisitos
    # Retornar None, 3 si la contraseña no cumple con los requisitos
    #

    user_tmp, no = buscar_usuario(username, password)

    if no != 1:
        return None, 1

    user = UsuarioRegistrado(username, password)

    if not user.username:
        return None, 2
    elif not user.password:
        return None, 3

    with open(os.path.join("csv", "usuarios.csv"), 'a', encoding="utf-8") as file:
        file.write(f"{user.username},{user.password}\n")

    return user, 0


# Agrega encomienda al final de csv/encomiendas.csv
def guardar_encomienda(e: Encomienda):
    with open(os.path.join("csv", "encomiendas.csv"), 'a', encoding="utf-8") as file:
        file.write(
            f"{e.nombre},{e.destinatario},{e.peso},{e.destino},{e.fecha},{e.estado}\n")

    return


# Devolver lista con todas las encomiendas de un usuario dado
# Devuelve todas las encomiendas por defecto
def buscar_encomiendas(username: str = "") -> list:
    encomiendas_devueltas = []

    with open(os.path.join("csv", "encomiendas.csv"), 'r', encoding="utf-8") as file:
        encomiendas = file.readlines()

        for e in encomiendas[1:]:
            actual = e.strip().split(',')

            # Filtrar encomiendas por usuario
            if actual[1] == username:
                encomiendas_devueltas.append(Encomienda(*actual))
            elif username == "":
                encomiendas_devueltas.append(Encomienda(*actual))

    return encomiendas_devueltas


# Devolver lista con todos los reclamos de csv/reclamos.csv
def buscar_reclamos() -> list:
    reclamos = []
    with open(os.path.join("csv", "reclamos.csv"), 'r', encoding="utf-8") as file:
        lineas = file.readlines()
        for r in lineas[1:]:
            reclamo = r.strip().split(',', maxsplit=2)
            actual = Reclamo(reclamo[0], reclamo[1], reclamo[2])
            reclamos.append(actual)

    return reclamos


# Agregar reclamo al final de csv/reclamos.csv
def guardar_reclamo(r: Reclamo):
    with open(os.path.join("csv", "reclamos.csv"), 'a', encoding="utf-8") as file:
        file.write(f"{r.usuario},{r.titulo},{r.descripcion}\n")

    return


# Sobreescribir archivo csv/encomiendas.csv dada una lista de encomiendas
def escribir_encomiendas(datos: list):
    with open(os.path.join("csv", "encomiendas.csv"), 'w', encoding="utf-8") as file:
        file.write("nombre_articulo,receptor,peso,destino,fecha,estado\n")

        for e in datos:
            linea = f"{e.nombre},{e.destinatario},{e.peso},{e.destino},{e.fecha},{e.estado}\n"
            file.write(linea)
