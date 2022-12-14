import sys
from os import path

from PyQt5.QtWidgets import QApplication
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_ranking import VentanaRanking
from frontend.ventana_post import VentanaPost

from backend.logica_principal import LogicaPrincipal
from backend.logica_juego import Juego


if __name__ == '__main__':
    app = QApplication([])
    # Importar archivo css
    with open(path.join("frontend", "style.css"), 'r') as file:
        stylesheet = app.setStyleSheet(file.read())

    # Instanciar ventanas
    ventana_inicio = VentanaInicio()
    ventana_ranking = VentanaRanking()
    ventana_principal = VentanaPrincipal()
    ventana_juego = VentanaJuego()
    ventana_post = VentanaPost()

    # Instanciar logicas
    logica_principal = LogicaPrincipal()
    logica_juego = Juego()

    # Señales ventanas
    # ventana inicio
    ventana_inicio.senal_ranking.connect(ventana_ranking.mostrar)
    ventana_inicio.senal_jugar.connect(ventana_principal.show)

    # ventana rakings
    ventana_ranking.senal_volver.connect(ventana_inicio.show)

    # ventana principal
    ventana_principal.senal_enviar_login.connect(logica_principal.comprobar_usuario)
    ventana_principal.senal_abrir_juego.connect(logica_juego.iniciar_juego)

    # ventana juego
    ventana_juego.senal_actualizar_teclas.connect(logica_juego.actualizar_teclas)
    ventana_juego.senal_boton_pausa.connect(logica_juego.pausar_juego)
    ventana_juego.senal_boton_volver.connect(logica_juego.boton_volver)
    ventana_juego.senal_boton_volver.connect(ventana_inicio.show)

    # ventana post-juego
    ventana_post.senal_siguiente_nivel.connect(logica_juego.iniciar_nivel)
    ventana_post.senal_menu_inicio.connect(ventana_inicio.show)

    # Señales lógicas
    # lógica juego
    logica_juego.senal_iniciar_juego.connect(ventana_juego.iniciar_nivel)
    logica_juego.senal_crear_aliens.connect(ventana_juego.agregar_label_alien)
    logica_juego.senal_actualizar_balas.connect(ventana_juego.actualizar_balas)
    logica_juego.senal_actualizar_tiempo.connect(ventana_juego.actualizar_tiempo)
    logica_juego.senal_terminar_nivel.connect(ventana_post.mostrar)
    logica_juego.senal_esconder_ventana_juego.connect(ventana_juego.hide)
    logica_juego.senal_terminator_god.connect(ventana_juego.fin_nivel)

    # Señales de instancias dentro de lógica_juego
    logica_juego.explotador.senal_explosion.connect(ventana_juego.explosion)
    logica_juego.explotador.senal_mover.connect(ventana_juego.mover_explosion)

    logica_juego.mira.senal_posicion.connect(ventana_juego.mover_mira)
    logica_juego.mira.senal_disparando.connect(ventana_juego.cambiar_mira)
    logica_juego.mira.senal_disparando.connect(logica_juego.disparar)

    logica_juego.bomba_hielo.senal_pos_bomba.connect(ventana_juego.mover_bomba)
    logica_juego.bomba_hielo.senal_estado_bomba.connect(ventana_juego.estado_bomba)

    logica_juego.estrella_muerte.senal_pos_estrella.connect(ventana_juego.mover_estrella)
    logica_juego.estrella_muerte.senal_estado_estrella.connect(ventana_juego.estado_estrella)

    # lógica ventana principal
    logica_principal.senal_respuesta_validacion.connect(ventana_principal.recibir_validacion)

    ventana_inicio.show()
    sys.exit(app.exec_())
