from flask import Flask
from app.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
# Instanciando o framework em uma variável manipulável
app.config.from_object(Config)
# Definição da configuração da aplicação com base na classe Config do módulo config 

Bootstrap(app)
# Permissão da edição dos templates com Bootstrap
login_manager = LoginManager()
# Instanciando o gerenciador de login em uma variável manipulável
login_manager.init_app(app)
# Iniciando o gerenciador

db = SQLAlchemy(app)
# Instanciando a extensão de comunicação entre banco de dados e o código/python

from app import routes
from app import forms
from app import models
# Após a criação da estrutura da aplicação, ela deve ser retrnada para ser utilizada