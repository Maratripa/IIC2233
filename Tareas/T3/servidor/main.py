import sys
from servidor import Servidor
from utils import data_json

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    servidor = Servidor(HOST, PORT)

    try:
        while True:
            input('|' + "[Presione Ctrl+c para cerrar]".center(80, '-') + '|' + '\n')
    except KeyboardInterrupt:
        print("\nCerrando servidor...\n".center(80, ' '))
        servidor.socket_servidor.close()
        sys.exit(0)
