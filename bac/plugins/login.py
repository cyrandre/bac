from flask_login import LoginManager
import click
import getpass
from .models import db,User
from datetime import datetime

login_manager = LoginManager()

@click.command("create-admin")
def create_admin():
  firstname = input("Enter your firstname: ")
  name = input("Enter your name: ")
  email = input("Enter email address: ")
  password = getpass.getpass("Enter password: ")
  confirm = getpass.getpass("Enter password again: ")
  if password != confirm:
    click.echo("Password don't match")
  else:
    try:
      user = User(
        firstname = firstname,
        name = name,
        email = email,
        password=password,
        is_admin=True,
        is_confirmed=True,
        confirmed_on = datetime.now(),
      )
      db.session.add(user)
      db.session.commit()
      click.echo(f"Admin with email {email} created successfully!")

    except Exception as err:
      # click.echo(f"Error {err}")
      click.echo("Couldn't create admin user.")

@login_manager.user_loader
def load_user(user_id):
  return User.query.filter(User.id == int(user_id)).first()

