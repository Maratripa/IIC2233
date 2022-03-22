import archivos
import funciones


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
