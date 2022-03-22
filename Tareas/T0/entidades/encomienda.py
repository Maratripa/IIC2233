from datetime import datetime


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
