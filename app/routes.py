from app import app, db
from flask import render_template, redirect, url_for, flash, request
from app.forms.login_form import LoginForm
from app.forms.usuario_form import UsuarioForm
from app.forms.servidor_form import ServidorForm
from app.controllers.authenticationController import AuthenticationController
from app.controllers.usuarioController import UsuarioController
from app.controllers.servidorController import ServidorController
from app.controllers.secretariaController import SecretariaController
from app.models import Secretaria, Cargo, Usuario



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


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        sucesso = UsuarioController.salvar(formulario)
        if sucesso:
            flash("Usuário cadastrado com sucesso!", category='success')
            return redirect(url_for('login'))
        else:
            flash("Erro ao cadastrar o novo usuário.", category='error')
            return render_template("cadastro.html", form = formulario)
    return render_template("cadastro.html", form=formulario)


@app.route('/listar', methods=['GET'])
def listar():
    lista_usuarios = UsuarioController.listar_usuarios()
    return render_template("listar.html", usuarios=lista_usuarios)


@app.route('/usuarios/<int:id>/edit', methods=['GET', 'POST'])
def usuarios_edit(id):
    usuario = Usuario.query.get(id)
    form = UsuarioForm(obj=usuario)
    if form.validate_on_submit():
        form.populate_obj(usuario)
        if form.password.data:
            usuario.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('listar'))  # ou a rota da lista
    return render_template('edit.html', form=form, usuario=usuario)



@app.route('/usuarios/<int:id>/delete', methods=['POST'])
def usuarios_delete(id):
    resultado = UsuarioController.remover_usuario(id)
    if resultado:
        flash('Usuário excluído com sucesso!', 'success')
    else:
        flash('Erro ao excluir usuário.', 'danger')
    return redirect(url_for('usuarios_index'))

"""
@app.route('/remover/<int:id>', methods=['GET'])
def remover_usuario(id):
    UsuarioController.remover_usuario(id)
    flash("Usuário removido com sucesso.", "success")
    return redirect(url_for("listar"))"""


@app.route('/servidores', methods=['GET', 'POST'])
def servidores():
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

    lista_servidores = ServidorController.listar()
    return render_template("servidores.html", form=form, servidores=lista_servidores)


@app.route('/remover_servidor/<int:id>', methods=['GET'])
def remover_servidor(id):
    ServidorController.remover(id)
    flash("Servidor removido com sucesso!", "success")
    return redirect(url_for("servidores"))


@app.route('/secretarias', methods=['GET', 'POST'])
def secretarias():
    from app.forms.secretaria_form import SecretariaForm
    form = SecretariaForm()

    if form.validate_on_submit():
        sucesso = SecretariaController.criar(form)
        if sucesso:
            flash("Secretaria cadastrada!", "success")
            return redirect(url_for("secretarias"))
        else:
            flash("Erro ao cadastrar secretaria.", "error")

    lista_secretarias = SecretariaController.listar()
    return render_template("secretarias.html", form=form, secretarias=lista_secretarias)
