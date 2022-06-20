import json
from os import path


def data_json(llave):
    """Lee parametros.json y retorna el valor del dato dada una llave"""
    ruta = path.join("parametros.json")
    with open(ruta, 'r', encoding="UTF-8") as f:
        diccionario_data = json.load(f)
    valor = diccionario_data[llave]
    return valor


def posicion_ficha(i, j) -> list:
    return [23 + 76 * j, 90 + 76 * i]

def posicion_estrella(i, j) -> list:
    return [35 + 76 * j, 89 + 76 * i]


def suma_centro(array: list) -> int:
    """Obtiene la suma de los bytes centrales"""
    l = len(array)

    if l == 1:
        suma = array[0]
    elif l % 2 == 0:
        suma = array[(l + 1) // 2] + array[(l + 1) // 2 - 1]
    else:
        centro = (l - 1) // 2
        suma = array[centro] + (array[centro - 1] + array[centro + 1]) // 2

    return suma


def encriptar_mensaje(mensaje_bytes: bytes) -> bytes:
    """Encriptar el mensaje"""
    A = []
    B = []
    j = 0
    i = 0
    segundo = False
    while len(A) + len(B) < len(mensaje_bytes):
        etapa = j % 4
        if etapa == 0:
            A.append(mensaje_bytes[i])
            j += 1
        elif etapa == 1:
            B.append(mensaje_bytes[i])
            j += 1
        elif etapa == 2:
            A.append(mensaje_bytes[i])
            if segundo:
                segundo = False
                j += 1
            else:
                segundo = True
        elif etapa == 3:
            B.append(mensaje_bytes[i])
            if segundo:
                segundo = False
                j += 1
            else:
                segundo = True
        i += 1

    mensaje = bytearray()
    if suma_centro(A) <= suma_centro(B):
        mensaje.extend(b'\x01')
        mensaje.extend(bytes(A))
        mensaje.extend(bytes(B))
    else:
        mensaje.extend(b'\x00')
        mensaje.extend(bytes(B))
        mensaje.extend(bytes(A))

    return bytes(mensaje)


def desencriptar_mensaje(mensaje_bytes: bytes) -> bytes:
    """Desencriptar el mensaje"""
    n = mensaje_bytes[0]
    mensaje_bytes = bytearray(mensaje_bytes[1:])

    l = len(mensaje_bytes)

    if l % 2 == 1:
        if n == 1:
            corte = (l - 1) // 2 + 1
            A = mensaje_bytes[:corte]
            B = mensaje_bytes[corte:]
        else:
            corte = (l - 1) // 2
            A = mensaje_bytes[corte:]
            B = mensaje_bytes[:corte]
    else:
        stop = l % 6
        if stop == 4:
            if n == 1:
                corte = l // 2 + 1
                A = mensaje_bytes[:corte]
                B = mensaje_bytes[corte:]
            else:
                corte = l // 2 - 1
                A = mensaje_bytes[corte:]
                B = mensaje_bytes[:corte]
        else:
            corte = l // 2
            if n == 1:
                A = mensaje_bytes[:corte]
                B = mensaje_bytes[corte:]
            else:
                A = mensaje_bytes[corte:]
                B = mensaje_bytes[:corte]

    mensaje = []
    totlen = len(A) + len(B)
    iters = l
    while len(mensaje) < totlen:
        etapa = iters % 6
        if etapa in {1, 3, 4}:
            mensaje.append(A.pop(-1))
        else:
            mensaje.append(B.pop(-1))

        iters -= 1

    return bytes(reversed(mensaje))
