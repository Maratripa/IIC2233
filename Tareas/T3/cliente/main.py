import sys

from PyQt5.QtWidgets import QApplication
from backend.cliente import Cliente
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    try:
        app = QApplication(sys.argv)

        cliente = Cliente(HOST, PORT)

        sys.exit(app.exec_())

    except ConnectionError as e:
        print("Ocurrio un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.socket_cliente.close()
        sys.exit(0)
