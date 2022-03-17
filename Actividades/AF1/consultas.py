from collections import namedtuple

Plato = namedtuple("Plato_type", ["nombre", "categoria", "tiempo", "precio", "ingredientes"])

# --- EJEMPLO --- #
# [Plato1, Plato2, Plato2, Plato4]
# pasa a ser
# {"Categoria1": [Plato3, Plato2], "Categoria2": [Plato1, Plato4]}
def platos_por_categoria(lista_platos: list) -> dict:
    return_dict = {}
    for plato in lista_platos:
        if plato.categoria in return_dict:
            return_dict[plato.categoria].append(plato)
        else:
            return_dict[plato.categoria] = [plato]
    
    return return_dict


# Debe devolver los platos que no tengan ninguno de los ingredientes descartados
def descartar_platos(ingredientes_descartados: set, lista_platos: list):
    returned_platos = []

    for plato in lista_platos:
        if len(plato.ingredientes & ingredientes_descartados) == 0:
            returned_platos.append(plato)
    
    return returned_platos


# --- EXPLICACION --- #
# Si el plato necesita un ingrediente que no tiene cantidad suficiente,
# entonces retorna False
#
# En caso que tenga todo lo necesario, resta uno a cada cantidad y retorna True
def preparar_plato(plato, ingredientes: dict) -> bool:
    for ingrediente_plato in plato.ingredientes:
        if ingredientes[ingrediente_plato] <= 0:
            return False

    for ingrediente_plato in plato.ingredientes:
        ingredientes[ingrediente_plato] -= 1

    return True


# --- EXPLICACION --- #
# Debe retornar un diccionario que agregue toda la información ...
#  de la lista de platos.
# precio total, tiempo total, cantidad de platos, platos
def resumen_orden(lista_platos: list) -> dict:
    return_dict = {
        "precio total" : 0,
        "tiempo total" : 0,
        "cantidad de platos" : 0,
        "platos" : []
    }

    for p in lista_platos:
        return_dict["precio total"] += p.precio
        return_dict["tiempo total"] += p.tiempo
        return_dict["cantidad de platos"] += 1
        return_dict["platos"].append(p.nombre)
    
    return return_dict

