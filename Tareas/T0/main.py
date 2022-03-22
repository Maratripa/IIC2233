import archivos
import parametros
import funciones

from entidades.administrador import Admin


def ingresar_usuario():
    #
    # Esta función ingresa al usuario y devuelve el menu del usuario ingresado,
    # o en su defecto, el menu inicial.
    #

    funciones.clear_screen()
    print("** Iniciar sesion **\n")

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

    return user.menu_usuario()


def ingresar_admin(errn=0):
    #
    # Esta función ingresa al administrador y devuelve su respectivo menú,
    # en caso de fallo devuelve el menu inicial.
    #

    funciones.clear_screen()
    print("** Iniciar sesion administrador **")

    def pedir_contrasena():
        #
        # Esta función local pide la contraseña hasta que se entregue la correcta o
        # se vuelva al menu de inicial.
        #

        contrasena = input("\nContrasena administrador: ")

        if contrasena != parametros.CONTRASENA_ADMIN:
            funciones.clear_screen()
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

    # Iniciar administrador con su menú
    admin = Admin()
    return admin.menu_administrador()


def registrar_usuario():
    #
    # Esta función se encarga de registrar un usuario y devolver su menú,
    # o en su defecto, el menú inicial.
    #

    funciones.clear_screen()
    print("** Registro de usuario **\n")

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

    return user.menu_usuario()


def menu_inicio(errn=0):
    #
    # Esta función se encarga de mostrar el menú inicial y el error asociado
    # (solo en caso que exista alguno).
    #

    if errn != 1000:
        funciones.clear_screen()

    errores = {
        0: "",
        1: "\nDebes ingresar un numero",
        2: "\nPor favor ingresa una opcion valida",
        3: "\nUsuario no registrado",
        4: "\nContrasena incorrecta",
        5: "\nUsuario ya registrado",
        6: "\nNombre de usuario no cumple con los requisitos",
        7: "\nContrasena no cumple con los requisitos",
        1000: "",
    }

    print("** Menu de Inicio **\n")
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
        ingresar_admin()
        return menu_inicio()
    elif opcion == 4:
        funciones.clear_screen()
        print("Gracias por utilizar DCCorreos de Chile\n")
        exit()
    else:
        return menu_inicio(2)


if __name__ == "__main__":
    print("\n*** Bienvenido a DCCorreos de Chile ***\n")
    menu_inicio(1000)
