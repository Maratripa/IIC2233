import archivos
import parametros


def ingresar_usuario():
    username = input("Usuario: ")
    passw = input("Contrasena: ")

    user, errn = archivos.buscar_usuario(username, passw)

    if errn == 1:
        return menu_inicio(3)
    elif errn == 2:
        return menu_inicio(4)

    user.menu_usuario()


def registrar_usuario():
    username = input(
        f"Usuario (min. {parametros.MIN_CARACTERES} caracteres): ")
    passw = input(
        f"Contrasena (min. {parametros.LARGO_CONTRASENA} caracteres): ")

    user, errn = archivos.registrar_usuario(username, passw)

    if errn == 1:
        return menu_inicio(5)
    elif errn == 2:
        return menu_inicio(6)
    elif errn == 3:
        return menu_inicio(7)

    user.menu_usuario()


def menu_inicio(errn=0):
    errores = {
        0: "",
        1: "\nDebes ingresar un numero",
        2: "\nPor favor ingresa una opcion valida",
        3: "\nUsuario no registrado",
        4: "\nContrasena incorrecta",
        5: "\nUsuario ya registrado",
        6: "\nNombre de usuario no cumple con los requisitos",
        7: "\nContrasena no cumple con los requisitos",
    }

    print("\n** Menu de Inicio **\n")
    print("[1] Iniciar sesion como usuario")
    print("[2] Registrarse como usuario")
    print("[3] Iniciar sesion como administrador")
    print("[4] Salir del programa")

    print(errores[errn])

    opcion = input("Indique la opcion elegida: ")

    if opcion.isnumeric():
        opcion = int(opcion)
    else:
        return menu_inicio(1)

    if opcion == 1:
        ingresar_usuario()
        return menu_inicio()
    elif opcion == 2:
        registrar_usuario()
        return menu_inicio()
    elif opcion == 3:
        menu_administrador()
        return menu_inicio()
    elif opcion == 4:
        return
    else:
        return menu_inicio(2)


def menu_administrador(errn=0):
    contrasena = input("\nContrasena administrador: ")

    if contrasena != parametros.CONTRASENA_ADMIN:
        return menu_inicio(4)

    errores = {
        0: "",
        1: "\nDebes ingresar un numero",
        2: "\nPor favor ingresa una opcion valida",
    }

    print("\n** Menu de administrador **\n")
    print("[1] Actualizar encomiendas")
    print("[2] Revisar reclamos")
    print("[3] Cerrar sesion")

    print(errores[errn])

    opcion = input("Ingrese la opcion elegida: ")

    if opcion.isnumeric():
        opcion = int(opcion)
    else:
        return menu_administrador(1)

    if opcion == 1:
        pass
    elif opcion == 2:
        pass
    elif opcion == 3:
        return
    else:
        return menu_administrador(2)


if __name__ == "__main__":
    print("\n---- Bienvenid@ a DCCorreos de Chile ----")
    print("\nSelecciona una de las siguientes opciones:")
    menu_inicio()
