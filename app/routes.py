from app import app
from flask import render_template, redirect
from app.forms import AnotacaoForm, UsuarioLogarForm, CadastroUsuarioForm, ListaAnotacoes, AtualizarAnotacaoForm
from app.models import AnotacaoModel, UserModel
from app import db
from app import login_manager
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug import secure_filename
import os

dicionario_de_error = {"Not a valid integer value": "O CPF deve conter somente números!"}

"""
O app.route é um Decorator ou Decorador, ele básicamente será utilizado por nós para atrelar ao endereço digitado no brownser a uma função e definir
o método HTTP aceito pela função.
No exemplo a baixo temos o endereço http://localhost:5000/ ou http://localhost:5000/index irá executar a função carregar_index().
"""
@app.route("/index", methods=['GET', 'POST'])
@app.route("/", methods=['GET', 'POST'])
def carregar_index():
    # A função render_template deve ser utilizada para carregar arquivos .html que possuam código Jinja.
    return render_template("index.html", title='Cu')


"""
O @login_required é um decorator do plugin flask_plugin que não precisa de nenhum parâmetro e verifica se existe algum usuário logado no sistema para poder executar a função que ele decora.
"""
@app.route("/perfil", methods=['GET', 'POST'])
@login_required
def carregar_perfil():
    anotacoes = AnotacaoModel.query.filter_by(usuario_id=current_user.cpf)
    return render_template("perfil.html",
                            title=current_user.nome, lista=anotacoes)

@app.route("/cadastrar_usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    form_cad_usuario = CadastroUsuarioForm()
    if form_cad_usuario.validate_on_submit():
        nome_arquivo = secure_filename(form_cad_usuario.foto.data.filename)
        form_cad_usuario.foto.data.save(
                                os.path.join(app.root_path + '/static/',
                                             nome_arquivo))
        novo_usuario = UserModel(
                            form_cad_usuario.cpf.data,
                            form_cad_usuario.nome.data,
                            form_cad_usuario.email.data,
                            form_cad_usuario.senha.data,
                            "fotos/"+nome_arquivo
                            )
        db.session.add(novo_usuario)
        db.session.commit()
        return redirect("/logar")
    return render_template("form_cadastro_usuario.html", form=form_cad_usuario, dic=dicionario_de_error)

@app.route("/cadastrar_anotacao",methods=['GET','POST'])
def cadastrar_anotacao():
    form = AnotacaoForm()
    if form.validate_on_submit():
        anotacao = AnotacaoModel(
                            form.titulo.data,
                            form.texto.data
                            )
        current_user.anotacoes.append(anotacao)
        db.session.merge(current_user)
        #add, merge, delete
        db.session.commit()
        return redirect('/perfil')
    return render_template("form_cadastro_anotacoes.html", form=form)

@app.route("/carregar_anotacoes",methods=['GET','POST'])
def carregar_anotacoes():
    form = ListaAnotacoes()
    atualizar = None
    if form.lista.data != "None":
        atualizar = AtualizarAnotacaoForm()
        anotacao = AnotacaoModel.query.filter_by(id=form.lista.data).first()
        atualizar.titulo.data = anotacao.titulo
        atualizar.texto.data = anotacao.texto
        atualizar.id.data = anotacao.id
        atualizar.data.data = anotacao.data
        
    form.lista.choices = []
    for anotacao in current_user.anotacoes:
        form.lista.choices.append((anotacao.id, anotacao.titulo))
        
    return render_template("atualizar_anotacao.html", form=form, atualizar=atualizar)

@app.route("/atualizar_anotacao",methods=['GET','POST'])
def atualizar_anotacao():
    form = AtualizarAnotacaoForm()

    anotacao = AnotacaoModel.query.filter_by(id=form.id.data).first()
    anotacao.titulo = form.titulo.data
    anotacao.texto = form.texto.data
    anotacao.data = form.data.data
    db.session.merge(anotacao)
    db.session.commit()
    return redirect("/carregar_anotacoes")

@app.route("/remover_anotacao",methods=['GET','POST'])
def remover_anotacao():
    form = ListaAnotacoes()
    if form.lista.data != "None":
        anotacao = AnotacaoModel.query.filter_by(id=form.lista.data).first()
        db.session.delete(anotacao)
        db.session.commit()
    
    form.lista.choices = []
    for anotacao in current_user.anotacoes:
        form.lista.choices.append((anotacao.id, anotacao.titulo))
    #Label do botão submit renomeado para Remover
    form.submit.label.text = "Remover"
        
    return render_template("remover_anotacao.html", form=form)


@app.route('/logar', methods=['GET', 'POST'])
def logar_usuario():
    form = UsuarioLogarForm()
    if form.validate_on_submit():
        usuario = UserModel.query.filter_by(nome=form.nome.data).first()
        if usuario is not None:
            if usuario.verificar_senha(form.senha.data):
                login_user(usuario)
                return redirect("/perfil")
    else:
        print(form.nome)
    return render_template("logar.html", form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def deslogar_usuario():
    logout_user()
    return render_template("index.html",  usuario = current_user)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>A página procurada ainda não foi implementada, tente outra vez mais tarde!.</p>", 404


@login_manager.user_loader
def load_user(cpf):
    return UserModel.query.filter_by(cpf=cpf).first()