import parametros
import archivos
import funciones
from datetime import datetime


class UsuarioRegistrado:

    def __init__(self, username, password):
        self.__username = None
        self.__password = None
        self.username = username
        self.password = password
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

    def menu_usuario(self, errn=0):
        errores = {
            0: "",
            1: "\nDebes ingresar un numero",
            2: "\nPor favor ingresa una opcion valida",
            100: "\nEncomienda ingresada exitosamente!",
        }

        print("\n** Menu de Usuario **\n")
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

    def ingresar_encomienda(self):
        def pedir_nombre():
            nombre_articulo = input(
                "Ingresa el nombre del articulo (sin ','): ")

            if not nombre_articulo or ',' in nombre_articulo:
                funciones.manejo_errores(pedir_nombre, self.menu_usuario, "")

            return nombre_articulo

        nombre_articulo = pedir_nombre()

        def pedir_destinatario():

            destinatario = input("Ingrese destinatario: ")

            user_tmp, no = archivos.buscar_usuario(destinatario, "")

            if not destinatario or no == 1:
                funciones.manejo_errores(
                    pedir_destinatario, self.menu_usuario, "")

            return destinatario

        destinatario = pedir_destinatario()

        def pedir_peso():
            peso = input("Ingrese el peso: ")

            if not peso or not peso.isnumeric():
                funciones.manejo_errores(pedir_peso, self.menu_usuario, "")
            else:
                peso = int(peso)

            if peso > parametros.MAX_PESO:
                funciones.manejo_errores(pedir_peso, self.menu_usuario, "")

            return peso

        peso = pedir_peso()

        def pedir_destino():
            destino = input("Ingrese el destino: ")

            if not destino or ',' in destino:
                funciones.manejo_errores(pedir_destino, self.menu_usuario, "")

            return destino

        destino = pedir_destino()

        encomienda = Encomienda(nombre_articulo, destinatario, peso, destino)

        archivos.guardar_encomienda(encomienda)
        self.encomiendas.append(encomienda)

        return self.menu_usuario(100)

    def revisar_encomiendas(self):

        funciones.mostrar_encomiendas(self.encomiendas)

        opcion = input("Apriete una tecla para volver: ")

        return self.menu_usuario()

    def realizar_reclamo(self):
        def pedir_titulo():
            titulo = input("Titulo del reclamo: ")

            if not titulo or ',' in titulo:
                funciones.manejo_errores(pedir_titulo, self.menu_usuario, "")

            return titulo

        titulo = pedir_titulo()

        def pedir_descripcion():
            desc = input("Descripcion del reclamo: ")

            if not desc:
                funciones.manejo_errores(
                    pedir_descripcion, self.menu_usuario, "")

            return desc

        descripcion = pedir_descripcion()

        reclamo = Reclamo(self.username, titulo, descripcion)

        archivos.guardar_reclamo(reclamo)

        return self.menu_usuario()

    def ver_estado(self):
        encontradas = archivos.buscar_encomiendas(self.username)

        funciones.mostrar_encomiendas(encontradas)

        opcion = input("Apriete una tecla para volver: ")

        return self.menu_usuario()


class Admin:

    def menu_administrador(self, errn=0):
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
            return self.menu_administrador(1)

        if opcion == 1:
            self.actualizar_encomiendas()
        elif opcion == 2:
            pass
        elif opcion == 3:
            return
        else:
            return self.menu_administrador(2)

    def actualizar_encomiendas(self):
        encomiendas = archivos.buscar_encomiendas()

        funciones.mostrar_encomiendas(encomiendas)

        print(f"\n{len(encomiendas) + 1} Volver\n")

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

        archivos.escribir_encomiendas(encomiendas)
        return self.menu_administrador()


class Encomienda:

    def __init__(self, nombre, destinatario, peso, destino, fecha=None, estado="Emitida"):
        self.nombre = nombre
        self.destinatario = destinatario
        self.peso = peso
        self.destino = destino

        if not fecha:
            self.fecha = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
        else:
            self.fecha = fecha

        self.estado = estado


class Reclamo:
    def __init__(self, usuario, titulo, descripcion):
        self.usuario = usuario
        self.titulo = titulo
        self.descripcion = descripcion
