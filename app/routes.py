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
from app.forms.perfil_form import PerfilForm
from app.forms.alterarsenha_form import AlterarSenhaForm
from app.forms.noticia_form import NoticiaForm
from app.controllers.cargoController import CargoController
from app.controllers.authenticationController import AuthenticationController
from app.controllers.usuarioController import UsuarioController
from app.controllers.servidorController import ServidorController
from app.controllers.secretariaController import SecretariaController
from app.controllers.noticiaController import NoticiaController
from app.models import Secretaria, Cargo, Usuario, Servidor, Prefeitura, Atividade
from app.utils.log import registrar_atividade
from flask_login import current_user, login_required
from app.auth.decorators import requires_roles
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import os



"""
@app.route("/")
def home():
    form = LoginForm()
    return render_template("login.html", form=form)"""


@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    formulario = LoginForm()
    if formulario.validate_on_submit():
        if AuthenticationController.login(formulario):
            registrar_atividade(f"Login realizado por '{formulario.username.data}'")
            flash("Login realizado com sucesso!", "success")
            next_page = request.args.get('next')
            if not next_page:
                next_page = url_for('dashboard')
            return redirect(next_page)
            """return redirect(url_for("home"))"""
        else:
            registrar_atividade(f"TENTATIVA FALHA de login para '{formulario.username.data}'")
            flash("Usuário ou senha inválidos.", "error")
    return render_template('login.html', title='Login', form=formulario)


@app.route('/logout')
@login_required
def logout():
    successo = AuthenticationController.logout()
    if not successo:
        flash("Erro ao realizar logout.", "error")
    else:
        registrar_atividade(f"Logout realizado por '{current_user.username}'")
        flash("Logout realizado com sucesso!", "success")
    return redirect(url_for("login"))


@app.route("/perfil")
@login_required
def perfil_usuario():
    usuario = current_user
    return render_template("perfil/perfil.html", usuario=usuario)


@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def perfil_editar():
    usuario = current_user
    form = PerfilForm(obj=usuario)

    if form.validate_on_submit():

        usuario.username = form.username.data
        usuario.email = form.email.data

        # Senha nova opcional
        if form.password.data:
            AuthenticationController.atualizar_senha(usuario, form.password.data)

        # FOTO DE PERFIL
        if form.foto.data:
            filename = secure_filename(form.foto.data.filename)
            path = os.path.join("app/static/uploads/perfis", filename)
            form.foto.data.save(path)
            usuario.foto = f"uploads/perfis/{filename}"

        db.session.commit()
        flash("Perfil atualizado com sucesso!", "success")
        return redirect(url_for("perfil_usuario"))

    return render_template("perfil/edit.html", form=form, usuario=usuario)


@app.route("/perfil/senha", methods=["GET", "POST"])
@login_required
def perfil_alterar_senha():
    form = AlterarSenhaForm()

    if form.validate_on_submit():
        nova_senha_hash = generate_password_hash(form.nova_senha.data)

        current_user.password_hash = nova_senha_hash
        db.session.commit()

        flash("Senha atualizada com sucesso!", "success")
        return redirect(url_for("perfil_usuario"))

    return render_template("perfil/senha.html", form=form)



@app.route('/usuarios/cadastrar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
def usuarios_cadastrar():
    formulario = UsuarioForm()
    if formulario.validate_on_submit():
        sucesso = UsuarioController.salvar(formulario)
        if sucesso:
            registrar_atividade(f"Usuário '{formulario.username.data}' cadastrado.")
            flash("Usuário cadastrado com sucesso!", category='success')
            return redirect(url_for('login'))
            """return redirect(url_for('login'))"""
        else:
            flash("Erro ao cadastrar o novo usuário.", category='error')
            return render_template("usuarios/cadastro.html", form = formulario)
    return render_template("usuarios/cadastro.html", form=formulario)


@app.route('/usuarios', methods=['GET'])
@login_required
@requires_roles("admin")
def usuarios_listar():
    lista_usuarios = UsuarioController.listar_usuarios()
    return render_template("usuarios/listar.html", usuarios=lista_usuarios)


@app.route('/usuarios/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@requires_roles("admin")
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
        registrar_atividade(f"Usuário ID {id} atualizado.")
        return redirect(url_for('usuarios_listar')) 
    return render_template('usuarios/edit.html', form=form, usuario=usuario)



@app.route('/usuarios/<int:id>/delete', methods=['POST'])
@login_required
@requires_roles("admin")
def usuarios_delete(id):
    resultado = UsuarioController.remover_usuario(id)
    if resultado:
        registrar_atividade(f"Usuário ID {id} removido.")
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
@login_required
@requires_roles("admin", "gestor")
def servidores_cadastrar():
    form = ServidorForm()
    cargos = Cargo.query.all()
    secretarias = Secretaria.query.all()
    form.cargo_id.choices = [(c.id, c.nome) for c in cargos]
    form.secretaria_id.choices = [(s.id, s.nome) for s in secretarias]
    if form.validate_on_submit():
        sucesso = ServidorController.criar(form)
        if sucesso:
            registrar_atividade(f"Servidor '{form.nome.data}' cadastrado.")
            flash("Servidor cadastrado com sucesso!", "success")
            return redirect(url_for("servidores_listar"))
        else:
            flash("Erro ao cadastrar servidor.", "error")

    return render_template("servidores/cadastro.html", form=form)


@app.route('/servidores', methods=['GET'])
@login_required
@requires_roles("admin", "gestor", "operador")
def servidores_listar():
    lista_servidores = ServidorController.listar()
    return render_template("servidores/servidores.html", servidores=lista_servidores) 


@app.route('/servidores/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin", "gestor")
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
        registrar_atividade(f"Servidor ID {id} atualizado.")
        flash("Servidor atualizado com sucesso!", "success")
        return redirect(url_for("servidores_listar"))
    return render_template("servidores/edit.html", form=form, servidor=servidor)


@app.route('/servidores/<int:id>/delete', methods=['POST'])
@login_required
@requires_roles("admin")
def servidores_delete(id):
    sucesso = ServidorController.remover(id)
    if sucesso:
        registrar_atividade(f"Servidor ID {id} removido.")
        flash("Servidor removido com sucesso!", "success")
    else:
        flash("Erro ao remover servidor.", "error")
    return redirect(url_for("servidores_listar"))


@app.route('/secretarias/cadastrar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin", "gestor")
def secretarias_cadastrar():
    form = SecretariaForm()
    if form.validate_on_submit():
        sucesso = SecretariaController.criar(form)
        if sucesso:
            registrar_atividade(f"Secretaria '{form.nome.data}' criada.")
            flash("Secretaria cadastrada!", "success")
            return redirect(url_for("secretarias_listar"))
        else:
            flash("Erro ao cadastrar secretaria.", "error")
    return render_template("secretarias/cadastro.html", form=form)


@app.route('/secretarias')
@login_required
@requires_roles("admin", "gestor", "operador")
def secretarias_listar():
    lista = SecretariaController.listar()
    return render_template('secretarias/secretarias.html', secretarias=lista)


@app.route('/secretarias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin", "gestor")
def secretarias_editar(id):
    secretaria = Secretaria.query.get_or_404(id)
    form = SecretariaEditForm(obj=secretaria)
    if form.validate_on_submit():
        if SecretariaController.atualizar(id, form):
            registrar_atividade(f"Secretaria ID {id} atualizada.")
            flash("Secretaria atualizada!", "success")
            return redirect(url_for('secretarias_listar'))
        else:
            flash("Erro ao atualizar.", "error")
    return render_template("secretarias/edit.html", form=form, secretaria=secretaria)


@app.route('/secretarias/<int:id>/delete', methods=['POST'])
@login_required
@requires_roles("admin")
def secretarias_delete(id):
    if SecretariaController.remover(id):
        registrar_atividade(f"Secretaria ID {id} removida.")
        flash("Secretaria removida!", "success")
    else:
        flash("Erro ao remover secretaria.", "error")
    return redirect(url_for('secretarias_listar'))


@app.route('/cargos/cadastrar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin", "gestor")
def cargos_cadastrar():
    form = CargoForm()
    if form.validate_on_submit():
        sucesso = CargoController.criar(form)
        if sucesso:
            registrar_atividade(f"Cargo '{form.nome.data}' cadastrado.")
            flash("Cargo cadastrado com sucesso!", "success")
            return redirect(url_for("cargos_listar"))
        else:
            flash("Erro ao cadastrar cargo.", "error")
    return render_template("cargos/cadastro.html", form=form)


@app.route('/cargos', methods=['GET'])
@login_required
@requires_roles("admin", "gestor", "operador")
def cargos_listar():
    lista_cargos = CargoController.listar()
    return render_template("cargos/cargos.html", cargos=lista_cargos)


@app.route('/cargos/<int:id>/editar', methods=['GET', 'POST'])
@login_required
@requires_roles("admin", "gestor")
def cargos_editar(id):
    cargo = Cargo.query.get_or_404(id)
    form = CargoEditForm(obj=cargo)
    if form.validate_on_submit():
        sucesso = CargoController.atualizar(id, form)
        if sucesso:
            registrar_atividade(f"Cargo ID {id} atualizado.")
            flash("Cargo atualizado com sucesso!", "success")
            return redirect(url_for('cargos_listar'))
        else:
            flash("Erro ao atualizar cargo.", "error")
    return render_template("cargos/edit.html", form=form, cargo=cargo)


@app.route('/cargos/<int:id>/delete', methods=['POST'])
@login_required
@requires_roles("admin")
def cargos_delete(id):
    sucesso = CargoController.remover(id)
    if sucesso:
        registrar_atividade(f"Cargo ID {id} removido.")
        flash("Cargo removido com sucesso!", "success")
    else:
        flash("Erro ao remover cargo.", "error")
    return redirect(url_for('cargos_listar'))


@app.route("/noticias/cadastrar", methods=["GET", "POST"])
@login_required
@requires_roles("admin", "gestor")
def noticias_cadastrar():
    form = NoticiaForm()
    if form.validate_on_submit():
        NoticiaController.criar(form)
        flash("Notícia publicada!", "success")
        registrar_atividade(f"Notícia publicada: {form.titulo.data}")
        return redirect(url_for("noticias_listar"))
    return render_template("noticias/cadastro.html", form=form)


@app.route("/noticias")
@login_required
def noticias_listar():
    lista = NoticiaController.listar()
    return render_template("noticias/noticia.html", noticias=lista)


@app.route("/noticias/<int:id>/delete", methods=["POST"])
@login_required
@requires_roles("admin")
def noticias_delete(id):
    NoticiaController.remover(id)
    registrar_atividade(f"Noticia ID {id} removido.")
    flash("Notícia removida!", "success")
    return redirect(url_for("noticias_listar"))


@app.route("/atividades")
@login_required
@requires_roles("admin")  
def atividades_listar():
    from app.controllers.atividadeController import AtividadeController
    atividades = AtividadeController.listar_todas()
    return render_template("atividades/atividade.html", atividades=atividades)


@app.route("/dashboard")
@login_required
def dashboard():
    total_usuarios = Usuario.query.count()
    total_servidores = Servidor.query.count()
    total_secretarias = Secretaria.query.count()
    total_cargos = Cargo.query.count()
    ultimos_usuarios = Usuario.query.order_by(Usuario.id.desc()).limit(5).all()
    ultimos_servidores = Servidor.query.order_by(Servidor.id.desc()).limit(5).all()
    atividades = Atividade.query.order_by(Atividade.data.desc()).limit(10).all()
    noticias = NoticiaController.listar(limit=5)


    # Dados para gráficos
    servidores_por_secretaria = (
        db.session.query(Secretaria.nome, db.func.count(Servidor.id))
        .join(Servidor, Servidor.secretaria_id == Secretaria.id)
        .group_by(Secretaria.nome)
        .all()
    )

    cargos_distribuicao = (
        db.session.query(Cargo.nome, db.func.count(Servidor.id))
        .join(Servidor, Servidor.cargo_id == Cargo.id)
        .group_by(Cargo.nome)
        .all()
    )

    return render_template(
        "index.html",
        total_usuarios=total_usuarios,
        total_servidores=total_servidores,
        total_secretarias=total_secretarias,
        total_cargos=total_cargos,
        servidores_por_secretaria=servidores_por_secretaria,
        cargos_distribuicao=cargos_distribuicao,
        ultimos_usuarios=ultimos_usuarios,
        ultimos_servidores=ultimos_servidores,
        atividades=atividades,
        noticias=noticias
    )