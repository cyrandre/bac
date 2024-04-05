from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

def check_is_confirmed(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user.is_confirmed is False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("accounts.inactive"))
        return view(*args, **kwargs)
    return wrapped_view

def logout_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for('index'))
        return view(*args, **kwargs)

    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(*args,**kwargs):        
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Your are not log in as admin", "warning")
            return redirect(url_for('index'))
        return view(*args,**kwargs)
    return wrapped_view
