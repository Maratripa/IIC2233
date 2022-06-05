import sys
from backend.cliente import Cliente
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    cliente = Cliente(HOST, PORT)
    try:
        while True:
            input("esperando...")

    except ConnectionError as e:
        print("Ocurrio un error.", e)
    except KeyboardInterrupt:
        print("\nCerrando cliente...")
        cliente.socket_cliente.close()
        sys.exit(0)
