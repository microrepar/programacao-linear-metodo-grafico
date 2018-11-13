"""Módulo de execução do servidor web no modo debug
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""

from app import app


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
