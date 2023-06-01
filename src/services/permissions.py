from functools import wraps

from flask_jwt_extended import get_jwt


def auth_required(allowed_roles: list[str] = []):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            token = get_jwt()
            user_permissions = token.get("permissions") or []
            is_superuser = token.get("is_superuser")

            if is_superuser is True:
                return fn(*args, **kwargs)

            elif set(user_permissions) & set(allowed_roles):
                return fn(*args, **kwargs)
            else:
                return {"message": "You are not authorized to perform this action"}, 403

        return decorator

    return wrapper