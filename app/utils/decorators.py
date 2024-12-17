from functools import wraps

from flask import redirect, url_for
from flask_login import current_user


def role_required(*roles):
    def wrapper(func):
        @wraps(func)  # Mantém o nome e docstring da rota original
        def decorated_view(*args, **kwargs):
            # 1. Check if the user is logged in

            if not current_user.is_authenticated:
                return redirect(url_for('login')) # Redirect to login if not authenticated

            # 2. Check if the user has any of the required roles
            user_roles = [role.name for role in current_user.roles]
            for role in roles:
                if role in user_roles:
                    return func(*args, **kwargs) # 3. If all checks pass, call the original route function

            return "Access Denied", 403  # Optionally, redirect to an error page

        return decorated_view
    return wrapper
