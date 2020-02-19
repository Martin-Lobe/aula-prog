from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class AnotacaoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement='ignore_fk')
    titulo = db.Column(db.String(32))
    usuario_id = db.Column(db.Integer, db.ForeignKey('user_model.cpf'))
    texto = db.Column(db.Text, nullable=False)
    usuario = db.relationship('UserModel', back_populates='anotacoes')
    data = db.Column(db.Date)

    def __init__(self, titulo, texto):
        self.titulo = titulo
        self.texto = texto


class UserModel(UserMixin, db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    caminho_foto = db.Column(db.String, nullable=True)
    anotacoes = db.relationship('AnotacaoModel', back_populates='usuario')

    def __init__(self, cpf, nome, email, senha, caminho_foto):
        self.cpf = cpf
        self.nome = nome
        self.email = email
        self.caminho_foto = caminho_foto
        self.criptografar_senha(senha)
        self._authenticated = False

    def get_id(self):
        return self.cpf


    def criptografar_senha(self, password):
        self.senha_hash = generate_password_hash(password)


    def verificar_senha(self, password):
        return check_password_hash(self.senha_hash, password)


#python3
#from app import db
#db.create_all()
#