import parametros
import archivos
import funciones
from datetime import datetime


# Clase de Usuario Registrado
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


# Clase de Administrador
class Admin:

    # Mostrar el menú del administrador y derivar a las respectivas funciones
    def menu_administrador(self, errn=0):
        errores = {
            0: "",
            1: "\nDebes ingresar un numero",
            2: "\nPor favor ingresa una opcion valida",
        }

        funciones.clear_screen()

        print("** Menu de administrador **\n")
        print("[1] Actualizar encomiendas")
        print("[2] Revisar reclamos")
        print("[3] Cerrar sesion")

        print(errores[errn])

        opcion = input("Ingrese la opcion elegida: ")

        if opcion.isnumeric():
            opcion = int(opcion)
        else:
            return self.menu_administrador(1)

        if opcion == 1:
            self.actualizar_encomiendas()
        elif opcion == 2:
            self.revisar_reclamos()
        elif opcion == 3:
            return
        else:
            return self.menu_administrador(2)

    # Muestra todas las encomiendas y actualiza el estado de la seleccionada
    def actualizar_encomiendas(self):
        funciones.clear_screen()

        print("** Actualizar encomiendas **\n")

        encomiendas = archivos.buscar_encomiendas()

        funciones.mostrar_encomiendas(encomiendas)

        print(f"[{len(encomiendas) + 1}] Volver\n")

        opcion = input("Ingrese la opcion elegida: ")

        if not opcion or not opcion.isnumeric():
            return self.actualizar_encomiendas()
        else:
            opcion = int(opcion)

        if (opcion - 1) in range(len(encomiendas)):
            encomienda = encomiendas[opcion - 1]
            encomienda.estado = funciones.cambiar_estado(encomienda)
        elif opcion == len(encomiendas) + 1:
            return self.menu_administrador()
        else:
            return self.actualizar_encomiendas()

        # Sobreescribir el archivo de encomiendas
        archivos.escribir_encomiendas(encomiendas)
        return self.menu_administrador()

    # Mostrar títulos de los reclamos y la descripción del seleccionado
    def revisar_reclamos(self):
        funciones.clear_screen()

        print("** Buzon de Reclamos **\n")
        print("* Elija uno de los siguientes reclamos para visualizar su descripcion *\n")

        reclamos = archivos.buscar_reclamos()
        for i in range(len(reclamos)):
            print(f"[{i+1}] {reclamos[i].titulo}")

        print(f"\n[{len(reclamos) + 1}] Volver\n")

        opcion = input("Ingrese la opcion elegida: ")

        if not opcion or not opcion.isnumeric():
            return self.revisar_reclamos()
        else:
            opcion = int(opcion)

        # Encontrar reclamo seleccionado y mostrar descripción
        if opcion in range(1, len(reclamos) + 1):
            funciones.clear_screen()
            print("* Reclamo *\n")
            print(f"-Titulo: {reclamos[opcion - 1].titulo}")
            print(f"-Descripcion: {reclamos[opcion -1].descripcion}\n")

            # Input para dejar la pantalla estática
            espera = input("Apriete una tecla para volver: ")
            return self.revisar_reclamos()
        elif opcion == len(reclamos) + 1:
            return self.menu_administrador()
        else:
            return self.revisar_reclamos()


# Clase de encomienda
class Encomienda:

    def __init__(self, nombre, destinatario, peso, destino, fecha=None, estado="Emitida"):
        self.nombre = nombre
        self.destinatario = destinatario
        self.peso = float(peso)
        self.destino = destino

        # Si es una encomienda previa, utilizar fecha guardada
        # Si es una encomienda nueva, guardar fecha y tiempo de creación
        if not fecha:
            self.fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        else:
            self.fecha = fecha

        self.estado = estado


# Clase de Reclamo
class Reclamo:
    def __init__(self, usuario, titulo, descripcion):
        self.usuario = usuario
        self.titulo = titulo
        self.descripcion = descripcion
