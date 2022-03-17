from collections import namedtuple
from unicodedata import name

Plato = namedtuple("Plato_type", ["nombre", "categoria", "tiempo", "precio", "ingredientes"])

# --- EXPLICACION --- #
# los datos vienen en este orden el el .csv:
# nombre,categoria,tiempo_preparacion,precio,ingrediente_1,...,ingrediente_n
def cargar_platos(ruta_archivo: str) -> list:
    with open("platos.csv", 'r') as file:
        return_list = []
        platos = file.readlines()
        for p in platos:
            line = p.strip().split(',')
            return_list.append(Plato(line[0], line[1], int(line[2]), int(line[3]), set(line[4].split(';'))))
        
        return return_list


# --- EXPLICACION --- #
# los datos vienen en este orden el el .csv:
# nombre,cantidad
def cargar_ingredientes(ruta_archivo: str) -> dict:
    with open("ingredientes.csv", 'r') as file:
        ingredientes = file.readlines()
        ll = []
        for i in ingredientes:
            ll.append(i.strip().split(','))
        
        return_dict = {k[0]:int(k[1]) for k in ll}
        return return_dict

