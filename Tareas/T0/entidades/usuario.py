from .. import parametros, archivos, funciones
from encomienda import Encomienda
from reclamo import Reclamo


class UsuarioRegistrado:

    def __init__(self, username, password):
        self.__username = None
        self.__password = None
        self.username = username
        self.password = password
        # Manejo de encomiendas creadas en la sesión
        self.encomiendas = []

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, value):
        if len(value) >= parametros.MIN_CARACTERES:
            self.__username = value

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, value):
        if len(value) >= parametros.LARGO_CONTRASENA:
            self.__password = value

    # Mostrar el menú de usuario y redirigir a las funciones respectivas
    def menu_usuario(self, errn=0):
        errores = {
            0: "",
            1: "\nDebes ingresar un numero",
            2: "\nPor favor ingresa una opcion valida",
            100: "\nEncomienda ingresada exitosamente!",
            101: "\nReclamo ingresado exitosamente!"
        }

        funciones.clear_screen()
        print("** Menu de Usuario **\n")
        print("[1] Hacer encomienda")
        print("[2] Revisar estado de encomiendas realizadas")
        print("[3] Realizar reclamo")
        print("[4] Ver el estado de los pedidos personales")
        print("[5] Cerrar sesion")

        print(errores[errn])

        opcion_usuario = input("Indique la opcion elegida: ")

        if opcion_usuario.isnumeric():
            opcion_usuario = int(opcion_usuario)
        else:
            return self.menu_usuario(1)

        if opcion_usuario == 1:
            self.ingresar_encomienda()
        elif opcion_usuario == 2:
            self.revisar_encomiendas()
        elif opcion_usuario == 3:
            self.realizar_reclamo()
        elif opcion_usuario == 4:
            self.ver_estado()
        elif opcion_usuario == 5:
            return
        else:
            return self.menu_usuario(2)

    # Crear nueva encomienda y guardarla si cumple con los requisitos
    def ingresar_encomienda(self):
        #
        # Esta función utiliza while-loops para repetir el input en caso de ser inválido
        #

        funciones.clear_screen()
        print("** Ingreso de encomienda **\n")

        nombre_articulo = input("Ingresa el nombre del articulo (sin ','): ")

        while not nombre_articulo or ',' in nombre_articulo:
            funciones.print_error("\nNombre no valido\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                nombre_articulo = input(
                    "\nIngresa el nombre del articulo (sin ','): ")
            elif opcion == 2:
                return self.menu_usuario()

        destinatario = input("Ingrese destinatario: ")
        # Buscar usuario para saber si existe o no con el código de error
        user_tmp, no = archivos.buscar_usuario(destinatario, "")

        while not destinatario or no == 1:
            funciones.print_error("\nDestinatario no encontrado\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                destinatario = input("\nIngrese destinatario: ")
                user_tmp, no = archivos.buscar_usuario(destinatario, "")
            elif opcion == 2:
                return self.menu_usuario()

        def revisar_peso(peso):
            # ---------------------------------------------------------------
            # En esta función local se hace uso de try/except para manejar el
            # caso donde el usuario ingrese un carácter no numérico
            # ---------------------------------------------------------------

            p = peso
            try:
                p = float(peso)
                if p > parametros.MAX_PESO:
                    return True
                else:
                    return False
            except ValueError:
                return True

        peso = input("Ingrese el peso (kg): ")

        while revisar_peso(peso):
            funciones.print_error("\nPeso no valido\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                peso = input("\nIngrese el peso (kg): ")
            elif opcion == 2:
                return self.menu_usuario()

        peso = float(peso)

        destino = input("Ingrese el destino: ")

        while not destino or ',' in destino:
            funciones.print_error("\nDestino no valido\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                destino = input("\nIngrese el destino: ")
            elif opcion == 2:
                return self.menu_usuario()

        encomienda = Encomienda(nombre_articulo, destinatario, peso, destino)

        # Guardar encomienda en lista de encomiendas creadas en sesión y en el archivo
        archivos.guardar_encomienda(encomienda)
        self.encomiendas.append(encomienda)

        return self.menu_usuario(100)

    # Mostrar las encomiendas creadas en sesión
    def revisar_encomiendas(self):
        funciones.clear_screen()
        funciones.mostrar_encomiendas(self.encomiendas)

        opcion = input("\nApriete una tecla para volver: ")

        return self.menu_usuario()

    def realizar_reclamo(self):
        funciones.clear_screen()
        print("** Realizar reclamo **\n")

        titulo = input("Titulo del reclamo: ")
        while not titulo or ',' in titulo:
            funciones.print_error("\nTitulo no valido\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                titulo = input("\nTitulo del reclamo: ")
            elif opcion == 2:
                return self.menu_usuario()

        descripcion = input("Descripcion del reclamo: ")
        while not descripcion:
            funciones.print_error("\nDescripcion no valdida\n")

            opcion = funciones.manejo_opciones(2)

            if opcion == 1:
                descripcion = input("\nDescripcion del reclamo: ")
            elif opcion == 2:
                return self.menu_usuario()

        reclamo = Reclamo(self.username, titulo, descripcion)

        archivos.guardar_reclamo(reclamo)

        return self.menu_usuario(101)

    def ver_estado(self):
        funciones.clear_screen()

        encontradas = archivos.buscar_encomiendas(self.username)

        funciones.mostrar_encomiendas(encontradas)

        # Input para dejar la pantalla estática
        opcion = input("Apriete una tecla para volver: ")

        return self.menu_usuario()
