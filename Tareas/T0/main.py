import archivos
import parametros
import funciones


def ingresar_usuario():
    username = input("Usuario: ")

    if not username:
        return menu_inicio(6)

    passw = input("Contrasena: ")

    if not passw:
        return menu_inicio(7)

    user, errn = archivos.buscar_usuario(username, passw)

    if errn == 1:
        return menu_inicio(3)
    elif errn == 2:
        return menu_inicio(4)

    user.menu_usuario()


def registrar_usuario():
    username = input(
        f"Usuario (min. {parametros.MIN_CARACTERES} caracteres): ")

    if not username or not username.isalpha():
        return menu_inicio(6)

    passw = input(
        f"Contrasena (min. {parametros.LARGO_CONTRASENA} caracteres): ")

    if not passw or not passw.isalnum():
        return menu_inicio(7)

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
    def pedir_contrasena():
        contrasena = input("\nContrasena administrador: ")

        if contrasena != parametros.CONTRASENA_ADMIN:
            print("Contrasena incorrecta, seleccione una opcion:\n")
            print("[1] Repetir contrasena")
            print("[2] Volver al menu de inicio\n")

            opcion_tmp = funciones.manejo_opciones(2)

            if opcion_tmp == 1:
                return pedir_contrasena()
            elif opcion_tmp == 2:
                return menu_inicio()

        return

    pedir_contrasena()

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
