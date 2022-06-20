import sys
from os import path

from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from utils import data_json

if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    HOST = data_json("HOST")
    PORT = data_json("PORT")
    try:
        app = QApplication(sys.argv)

        with open(path.join("frontend", "style.css"), "r") as f:
            app.setStyleSheet(f.read())

        cliente = Cliente(HOST, PORT)

        app.exec()

    except ConnectionError as e:
        print("Ocurrio un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.socket_cliente.close()
        sys.exit(0)
