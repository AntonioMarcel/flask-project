import os
import sys

# Ajusta o caminho do PYTHONPATH para o diretório raiz da aplicação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
from app.models import Role

with app.app_context():
  roles = {1: "Admin", 2: "Liquidador", 3: "Pagador"}

  for key, role_name in roles.items():
    role = Role(name=role_name)
    db.session.add(role)

    db.session.commit()


# from functools import wraps
# from flask import abort
# from flask_login import current_user

# def role_required(role_name):
#     """
#     Verifica se o usuário logado possui uma função específica.
#     :param role_name: Nome da função necessária para acessar a rota.
#     """
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             # Verifica se o usuário está autenticado
#             if not current_user.is_authenticated:
#                 abort(401)  # Retorna "401 Unauthorized" se não autenticado

#             # Verifica se o usuário possui a função necessária
#             user_roles = [role.name for role in current_user.roles]  # Obtém os nomes das funções
#             if role_name not in user_roles:
#                 abort(403)  # Retorna "403 Forbidden" se não autorizado

#             # Se tudo estiver ok, executa a função original
#             return func(*args, **kwargs)
#         return wrapper
#     return decorator
