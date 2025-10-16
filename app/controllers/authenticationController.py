from app.models.usuario import Usuario
from werkzeug.security import check_password_hash
from flask_login import login_user

class AuthenticationController:

    @staticmethod
    def login(form):
        username = form.username.data.strip()
        user = Usuario.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return True
        return False
