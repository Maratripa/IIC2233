import parametros
import archivos
import funciones
from datetime import date


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
            3: "\nNombre del articulo no cumple con los requisitos",
            4: "\nDestinatario no valido",
            5: "\nValor no valido",
            6: f"\nPeso mayor que el maximo permitido ({parametros.MAX_PESO})",
            7: "\nDestino no valido",
            100: "\nEncomienda ingresada exitosamente!",
        }

        print("\n** Menu de Usuario **\n")
        print("[1] Hacer encomienda")
        print("[2] Revisar estado de encomiendas realizadas")
        print("[3] Realizar reclamos")
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
            pass
        elif opcion_usuario == 4:
            pass
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
        print("* Encomiendas registradas *\n")
        print("|\tNombre articulo\t|\tReceptor\t|\tPeso\t|\tDestino\t|\tEstado\t|")

        for i in range(len(self.encomiendas)):
            actual = self.encomiendas[i]
            print(
                f"|\t{actual.nombre}\t|\t{actual.destinatario}\t\t|\t{actual.peso}\t|\t{actual.destino}\t|\t{actual.estado}\t|")

        opcion = input("Apriete una tecla para volver: ")

        return self.menu_usuario()


class Encomienda:

    def __init__(self, nombre, destinatario, peso, destino, estado="Emitida"):
        self.nombre = nombre
        self.destinatario = destinatario
        self.peso = peso
        self.destino = destino
        self.fecha = date.today().strftime("%Y/%m/%d")
        self.estado = estado
