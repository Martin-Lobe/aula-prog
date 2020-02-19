import os

caminho_modulo = os.path.abspath(os.path.dirname(__file__))
# Definição do caminho absoluto até esse módulo

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'qualquersenha'
    # Chave requerida pelo flask_wtf
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    "sqlite:///" + os.path.join(caminho_modulo, 'aplicacao.db')
    # Caminho no qual vai criar o arquivo que armazenará o BD
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Possibilita a modificação no BD


"""
SECRET_KEY = 'adJKkjhJK%4*3!af'
SQLALCHEMY_DATABASE_URI = 'sqlite:///sistema_anotacoes.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

ERRO GROTESCO: DEFINIÇÃO DE UM CAMINHO DO BD
QUE SÓ EXISTE NA MÁQUINA ONDE FOI CRIADO

UPLOAD_FOLDER = "/mnt/486333c2-f1b5-4b12-a490-67e4c68124a5/riad.nassiffe@ifc.edu.br/2019/medio/programacao/codigos/gerenciador_de_anotacoes/app/static/fotos/"
"""
