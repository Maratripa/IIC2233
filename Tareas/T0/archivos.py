import entidades


def buscar_usuario(username: str, password: str):
    users_dict = {}

    with open("usuarios.csv", 'r', encoding="utf-8") as file:
        users = file.readlines()

        for user in users[1:]:
            u = user.strip().split(',')
            users_dict[u[0]] = u[1]

    if username not in users_dict:
        return None, 1

    if password != users_dict[username]:
        return None, 2

    return entidades.UsuarioRegistrado(username, password), 0


def registrar_usuario(username: str, password: str):
    user_tmp, no = buscar_usuario(username, password)

    if no != 1:
        return None, 1

    user = entidades.UsuarioRegistrado(username, password)

    if not user.username:
        return None, 2
    elif not user.password:
        return None, 3

    with open("usuarios.csv", 'a', encoding="utf-8") as file:
        file.write(f"{user.username},{user.password}\n")

    return user, 0


def guardar_encomienda(e: entidades.Encomienda):
    with open("encomiendas.csv", 'a', encoding="utf-8") as file:
        file.write(
            f"{e.nombre},{e.destinatario},{e.peso},{e.destino},{e.fecha},{e.estado}\n")

    return


def buscar_encomiendas(username: str = "") -> list:
    encomiendas_devueltas = []

    with open("encomiendas.csv", 'r', encoding="utf-8") as file:
        encomiendas = file.readlines()

        for e in encomiendas[1:]:
            actual = e.strip().split(',')

            if actual[1] == username:
                encomiendas_devueltas.append(entidades.Encomienda(*actual))
            elif username == "":
                encomiendas_devueltas.append(entidades.Encomienda(*actual))

    return encomiendas_devueltas


def buscar_reclamos() -> list:
    reclamos = []
    with open("reclamos.csv", 'r', encoding="utf-8") as file:
        lineas = file.readlines()
        for r in lineas[1:]:
            reclamo = r.strip().split(',', maxsplit=2)
            actual = entidades.Reclamo(reclamo[0], reclamo[1], reclamo[2])
            reclamos.append(actual)

    return reclamos


def guardar_reclamo(r: entidades.Reclamo):
    with open("reclamos.csv", 'a', encoding="utf-8") as file:
        file.write(f"{r.usuario},{r.titulo},{r.descripcion}\n")

    return


def escribir_encomiendas(datos: list):
    with open("encomiendas.csv", 'w', encoding="utf-8") as file:
        file.write("nombre_articulo,receptor,peso,destino,fecha,estado\n")
        for e in datos:
            linea = f"{e.nombre},{e.destinatario},{e.peso},{e.destino},{e.fecha},{e.estado}\n"
            file.write(linea)
