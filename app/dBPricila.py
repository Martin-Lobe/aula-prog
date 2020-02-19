from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Vagas(db.Model):
    id = db.Column(db.Integer, primary_key=True,  autoincrement='ignore_fk')
    titulo = db.Column(db.String(32))
    empresa_id = db.Column(db.Integer, db.ForeignKey('usuario_empresa.cnpj'))
    texto = db.Column(db.Text, nullable=False)
    empresa = db.relationship('UsuarioEmpresa', back_populates='vagas')
    data = db.Column(db.Date)
    candidato_id = db.Column(db.Integer, db.ForeignKey('usuario_pessoa.cpf'))
    candidatos = db.relationship('UsuarioPessoa',
                                  back_populates='vagas')

class UsuarioEmpresa(UserMixin, db.Model):
    cnpj = db.Column(db.Integer, primary_key=True)
    pau = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    caminho_foto = db.Column(db.String, nullable=True)
    vagas = db.relationship('Vagas', back_populates='empresa')

    def __init__(self, cnpj, nome, email, senha, caminho_foto):
        self.cnpj = cnpj
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


class UsuarioPessoa(UserMixin, db.Model):
    cpf = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    senha_hash = db.Column(db.String(128))
    caminho_foto = db.Column(db.String, nullable=True)
    vagas = db.relationship('Vagas', back_populates='candidatos')

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
"""
from app import dBPricila
up1 = dBPricila.UsuarioPessoa(1,"pedro","","a","a") 

emp1 = dBPricila.UsuarioEmpresa(2,"googl","","a","a")
v1 = dBPricila.Vagas()
v1.titulo = "1"
v1.texto = "asdf"
v1.data = "01-10-2019"
v2 = dBPricila.Vagas()
v2.titulo = "2"
v2.texto = "asdf"
v2.data = datetime.datetime.now()
v3 = dBPricila.Vagas()
v3.titulo = "3"
emp1 = dBPricila.UsuarioEmpresa.query.filter_by(cnpj=2).first()
emp1.vagas.append(v1)
emp1.vagas.append(v2)
emp1.vagas.append(v3)
dBPricila.db.session.merge(emp1)
dBPricila.db.session.commit()
"""
