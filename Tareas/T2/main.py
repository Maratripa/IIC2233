import sys

from os import path
from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_ranking import VentanaRanking

from backend.logica_principal import LogicaPrincipal

import parametros as p


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])

    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_principal = VentanaPrincipal()
    ventana_juego = VentanaJuego(path.join(*p.RUTA_GALAXIA), 3, 60, 100)

    logica_principal = LogicaPrincipal()

    # Señales
    ventana_inicio.senal_ranking.connect(ventana_ranking.show)
    ventana_inicio.senal_jugar.connect(ventana_principal.show)

    ventana_ranking.senal_volver.connect(ventana_inicio.show)

    ventana_principal.senal_enviar_login.connect(logica_principal.comprobar_usuario)

    logica_principal.senal_respuesta_validacion.connect(ventana_principal.recibir_validacion)

    ventana_inicio.show()
    app.exec()
