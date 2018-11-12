"""Inicializador do pacote app
FATEC - MC - Autor: MCSilva - 03/11/2018 - Versão: 0.0.1
"""
from flask import Flask, session
from config import Config


app = Flask(__name__)
app.config.from_object(Config)


from app import routes, servicoweb, metodografico
