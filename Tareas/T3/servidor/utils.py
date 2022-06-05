import json
from os import path


def data_json(llave):
    """Lee parametros.json y retorna el valor del dato dada una llave"""
    ruta = path.join("parametros.json")
    with open(ruta, 'r', encoding="UTF-8") as f:
        diccionario_data = json.load(f)
    valor = diccionario_data[llave]
    return valor
