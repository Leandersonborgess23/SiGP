from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.usuario_form import UsuarioForm
from app.forms.servidor_form import ServidorForm
from app.forms.cargo_form import CargoForm
from app.forms.secretaria_form import SecretariaForm
from app.forms.usuarioedit_form import UsuarioEditForm
from app.forms.secretariaedit_form import SecretariaEditForm
from app.forms.cargoedit_form import CargoEditForm
from app.controllers.cargoController import CargoController
from app.controllers.authenticationController import AuthenticationController
from app.controllers.usuarioController import UsuarioController
from app.controllers.servidorController import ServidorController
from app.controllers.secretariaController import SecretariaController
from app.models import Secretaria, Cargo, Usuario, Servidor, Prefeitura
#from flask_login import current_user



@app.route("/")
def home():
    return render_template("index.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    formulario = LoginForm()
    if formulario.validate_on_submit():
        if AuthenticationController.login(formulario):
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('home')
            return redirect(next_page)
            """return redirect(url_for("home"))"""
        else:
            flash("Usuário ou senha inválidos.", "error")
    return render_template('login.html', title='Login', form=formulario)


@app.route('/logout')
def logout():
    successo = AuthenticationController.logout()
    if not successo:
        flash("Erro ao realizar logout.", "error")
    else:
        flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))


@app.route('/usuarios/cadastrar', methods=['GET', 'POST'])
def usuarios_cadastrar():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        sucesso = UsuarioController.salvar(formulario)
        if sucesso:
            flash("Usuário cadastrado com sucesso!", category='success')
            return redirect(url_for('login'))
            """return redirect(url_for('login'))"""
        else:
            flash("Erro ao cadastrar o novo usuário.", category='error')
            return render_template("usuarios/cadastro.html", form = formulario)
    return render_template("usuarios/cadastro.html", form=formulario)


@app.route('/usuarios', methods=['GET'])
def usuarios_listar():
    lista_usuarios = UsuarioController.listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=lista_usuarios)


@app.route('/usuarios/<int:id>/edit', methods=['GET', 'POST'])
def usuarios_edit(id):
    usuario = Usuario.query.get(id)
    form = UsuarioEditForm(obj=usuario)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        UsuarioController.atualizar_usuario(id, form)
        #form.populate_obj(usuario)
        """if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)"""
        #db.session.commit()
        #flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios_listar')) 
    return render_template('usuarios/edit.html', form=form, usuario=usuario)



@app.route('/usuarios/<int:id>/delete', methods=['POST'])
def usuarios_delete(id):
    resultado = UsuarioController.remover_usuario(id)
    if resultado:
        flash('Usuário excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir usuário.', 'danger')
    return redirect(url_for('usuarios_listar'))

"""
@app.route('/remover/<int:id>', methods=['GET'])
def remover_usuario(id):
    UsuarioController.remover_usuario(id)
    flash("Usuário removido com sucesso.", "success")
    return redirect(url_for("listar"))"""


@app.route('/servidores/cadastrar', methods=['GET', 'POST'])
def servidores_cadastrar():
    form = ServidorForm()
    cargos = Cargo.query.all()
    secretarias = Secretaria.query.all()
    form.cargo_id.choices = [(c.id, c.nome) for c in cargos]
    form.secretaria_id.choices = [(s.id, s.nome) for s in secretarias]
    if form.validate_on_submit():
        sucesso = ServidorController.criar(form)
        if sucesso:
            flash("Servidor cadastrado com sucesso!", "success")
            return redirect(url_for("servidores"))
        else:
            flash("Erro ao cadastrar servidor.", "error")

    return render_template("servidores/cadastro.html", form=form)


@app.route('/servidores', methods=['GET'])
def servidores_listar():
    lista_servidores = ServidorController.listar()
    return render_template("servidores/servidores.html", servidores=lista_servidores) 


@app.route('/servidores/<int:id>/editar', methods=['GET', 'POST'])
def servidores_editar(id):
    servidor = Servidor.query.get(id)
    if not servidor:
        flash("Servidor não encontrado.", "error")
        return redirect(url_for("servidores_listar"))
    form = ServidorForm(obj=servidor)
    cargos = Cargo.query.all()
    secretarias = Secretaria.query.all()
    form.cargo_id.choices = [(c.id, c.nome) for c in cargos]
    form.secretaria_id.choices = [(s.id, s.nome) for s in secretarias]
    if form.validate_on_submit():
        ServidorController.atualizar(id, form)
        flash("Servidor atualizado com sucesso!", "success")
        return redirect(url_for("servidores_listar"))
    return render_template("servidores/edit.html", form=form, servidor=servidor)


@app.route('/servidores/<int:id>/delete', methods=['POST'])
def servidores_delete(id):
    sucesso = ServidorController.remover(id)
    if sucesso:
        flash("Servidor removido com sucesso!", "success")
    else:
        flash("Erro ao remover servidor.", "error")
    return redirect(url_for("servidores_listar"))


@app.route('/secretarias/cadastrar', methods=['GET', 'POST'])
def secretarias_cadastrar():
    form = SecretariaForm()
    if form.validate_on_submit():
        sucesso = SecretariaController.criar(form)
        if sucesso:
            flash("Secretaria cadastrada!", "success")
            return redirect(url_for("secretarias_listar"))
        else:
            flash("Erro ao cadastrar secretaria.", "error")
    return render_template("secretarias/cadastro.html", form=form)


@app.route('/secretarias')
def secretarias_listar():
    lista = SecretariaController.listar()
    return render_template('secretarias/secretarias.html', secretarias=lista)


@app.route('/secretarias/<int:id>/editar', methods=['GET', 'POST'])
def secretarias_editar(id):
    secretaria = Secretaria.query.get_or_404(id)
    form = SecretariaEditForm(obj=secretaria)
    if form.validate_on_submit():
        if SecretariaController.atualizar(id, form):
            flash("Secretaria atualizada!", "success")
            return redirect(url_for('secretarias_listar'))
        else:
            flash("Erro ao atualizar.", "error")
    return render_template("secretarias/edit.html", form=form, secretaria=secretaria)


@app.route('/secretarias/<int:id>/delete', methods=['POST'])
def secretarias_delete(id):
    if SecretariaController.remover(id):
        flash("Secretaria removida!", "success")
    else:
        flash("Erro ao remover secretaria.", "error")
    return redirect(url_for('secretarias_listar'))


@app.route('/cargos/cadastrar', methods=['GET', 'POST'])
def cargos_cadastrar():
    form = CargoForm()
    if form.validate_on_submit():
        sucesso = CargoController.criar(form)
        if sucesso:
            flash("Cargo cadastrado com sucesso!", "success")
            return redirect(url_for("cargos_listar"))
        else:
            flash("Erro ao cadastrar cargo.", "error")
    return render_template("cargos/cadastro.html", form=form)


@app.route('/cargos', methods=['GET'])
def cargos_listar():
    lista_cargos = CargoController.listar()
    return render_template("cargos/cargos.html", cargos=lista_cargos)


@app.route('/cargos/<int:id>/editar', methods=['GET', 'POST'])
def cargos_editar(id):
    cargo = Cargo.query.get_or_404(id)
    form = CargoEditForm(obj=cargo)
    if form.validate_on_submit():
        sucesso = CargoController.atualizar(id, form)
        if sucesso:
            flash("Cargo atualizado com sucesso!", "success")
            return redirect(url_for('cargos_listar'))
        else:
            flash("Erro ao atualizar cargo.", "error")
    return render_template("cargos/edit.html", form=form, cargo=cargo)


@app.route('/cargos/<int:id>/delete', methods=['POST'])
def cargos_delete(id):
    sucesso = CargoController.remover(id)
    if sucesso:
        flash("Cargo removido com sucesso!", "success")
    else:
        flash("Erro ao remover cargo.", "error")
    return redirect(url_for('cargos_listar'))

