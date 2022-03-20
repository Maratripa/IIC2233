import entidades


def buscar_usuario(username, password):
    users_dict = {}

    with open("usuarios.csv", 'r') as file:
        users = file.readlines()

        for user in users[1:]:
            u = user.strip().split(',')
            users_dict[u[0]] = u[1]

    if username not in users_dict:
        return None, 1

    if password != users_dict[username]:
        return None, 2

    return entidades.UsuarioRegistrado(username, password), 0


def registrar_usuario(username, password):
    user_tmp, no = buscar_usuario(username, password)

    if no != 1:
        return None, 1

    user = entidades.UsuarioRegistrado(username, password)

    if not user.username:
        return None, 2
    elif not user.password:
        return None, 3

    with open("usuarios.csv", 'a') as file:
        file.write(f"{user.username},{user.password}\n")

    return user, 0


def guardar_encomienda(encomienda):
    pass
