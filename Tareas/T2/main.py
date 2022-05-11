import sys
from os import path

from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_ranking import VentanaRanking

from backend.logica_principal import LogicaPrincipal
from backend.logica_juego import Juego

import parametros as p


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    # Importar archivo css
    with open(path.join("frontend", "style.css"), 'r') as file:
        stylesheet = app.setStyleSheet(file.read())

    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_principal = VentanaPrincipal()
    ventana_juego = VentanaJuego()

    logica_principal = LogicaPrincipal()

    logica_juego = Juego()

    # Señales
    ventana_inicio.senal_ranking.connect(ventana_ranking.show)
    ventana_inicio.senal_jugar.connect(ventana_principal.show)

    ventana_ranking.senal_volver.connect(ventana_inicio.show)

    ventana_principal.senal_enviar_login.connect(logica_principal.comprobar_usuario)
    logica_principal.senal_respuesta_validacion.connect(ventana_principal.recibir_validacion)
    ventana_principal.senal_abrir_juego.connect(logica_juego.iniciar_nivel)

    logica_juego.senal_iniciar_juego.connect(ventana_juego.iniciar_nivel)

    ventana_juego.senal_actualizar_teclas.connect(logica_juego.actualizar_teclas)

    logica_juego.senal_crear_alien.connect(ventana_juego.agregar_label_alien)

    logica_juego.mira.senal_posicion.connect(ventana_juego.mover_mira)
    logica_juego.mira.senal_disparando.connect(ventana_juego.cambiar_mira)
    logica_juego.mira.senal_disparando.connect(logica_juego.disparar)

    ventana_inicio.show()
    app.exec()
