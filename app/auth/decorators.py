from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Você precisa fazer login.", "warning")
                return redirect(url_for("login"))

            if current_user.role not in roles:
                flash("Acesso negado!", "danger")
                return redirect(url_for("home"))

            return f(*args, **kwargs)
        return wrapped
    return wrapper
