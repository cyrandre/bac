
from flask import Blueprint,redirect,render_template,url_for
from flask import request,flash
from flask_login import current_user, login_required, login_user, logout_user
from datetime import datetime

from bac.plugins.email import send_email
from bac.plugins.models import User,db,bcrypt

from bac.utils.decorators import logout_required
from bac.utils.token import generate_token, confirm_token
from bac.utils.forms import RegisterForm, LoginForm

bp = Blueprint('accounts',__name__,url_prefix='/accounts')

@bp.before_app_request
def update_last_connection():
    if current_user.is_authenticated:
        User.query.filter_by(id=current_user.id).update(
            {'last_connection': datetime.now()}
        )

@bp.route("/register", methods=("GET", "POST"))
@logout_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():

        delete_user(email=form.email.data)
        # user = User.query.filter_by(email=form.email.data).first()
        # if user is not None:
        #     login_user(user)
        #     return redirect(url_for("accounts.resend_confirmation"))
        
        user = User(firstname=form.firstname.data,
                    name=form.name.data,
                    email=form.email.data, 
                    password=form.password.data,
                    job = form.job.data,
                    is_confirmed= False,
                    confirmed_on= datetime.now())
        
        db.session.add(user)
        db.session.commit()    
        token = generate_token(user.email)
        confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
        html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
        subject = "Please confirm your email"
        send_email(user.email, subject, html)
        login_user(user)

        flash("A confirmation email has been sent via email.", "success")
        return redirect(url_for("accounts.inactive"))

    return render_template("accounts/register.html", form=form)

@bp.route("/login", methods=("POST",))
@logout_required
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            print(f'Log in {user.firstname}')
            login_user(user,remember = form.remember)            
        else:
            print("Invalid email and/or password.", "danger")
    else:
        print('Form not validate')
    return redirect(url_for('index'))

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    print("You were logged out.", "success")
    return redirect(url_for("index"))

@bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        print("Account already confirmed.", "success")
        return redirect(url_for("index"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        print("You have confirmed your account. Thanks!", "success")
    else:
        print("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("index"))

@bp.route("/inactive")
@login_required
def inactive():
    if current_user.is_confirmed:
        return redirect(url_for("index"))
    return render_template("accounts/inactive.html")

@bp.route("/resend")
@login_required
def resend_confirmation():
    if current_user.is_confirmed:
        print("Your account has already been confirmed.", "success")
        return redirect(url_for("index"))
    token = generate_token(current_user.email)
    confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
    html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(current_user.email, subject, html)
    print("A new confirmation email has been sent.", "success")
    return redirect(url_for("accounts.inactive"))

def delete_user(email):
    User.query.filter_by(email=email).delete()