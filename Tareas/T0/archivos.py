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
