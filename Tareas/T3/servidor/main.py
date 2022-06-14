import sys
from servidor import Servidor
from utils import data_json, log

if __name__ == "__main__":
    HOST = data_json("HOST")
    PORT = data_json("PORT")
    servidor = Servidor(HOST, PORT)

    try:
        while True:
            input('|' + "[Presione Ctrl+c para cerrar]".center(80, '-') + '|' + '\n\n')
    except KeyboardInterrupt:
        log("\nCerrando servidor...\n")
        servidor.socket_servidor.close()
        sys.exit(0)
