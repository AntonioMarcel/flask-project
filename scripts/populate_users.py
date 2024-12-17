import os
import sys

# Ajusta o caminho do PYTHONPATH para o diretório raiz da aplicação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import select

from app import app, db
from app.models import User, Role

with app.app_context():
    users = [
        {
            "username": "xarope_wars",
            "email": "xarope_wars@gmail.com",
            "password": "123",
            "role": 1,
        },
        {
            "username": "pdidi",
            "email": "pdidi@gmail.com",
            "password": "123",
            "role": 2,
        },
        {
            "username": "xarope_von_britania",
            "email": "britania@gmail.com",
            "password": "123",
            "role": 3,
        },
    ]

    for user in users:
        u = User(username=user["username"], email=user["email"])
        u.set_password(user["password"])

        #Get and set user role
        query = select(Role).where(Role.id == user["role"])
        role = db.session.scalar(query)
        u.roles.append(role)

        db.session.add(u)

    db.session.commit()

    #modify for accepting more than one role