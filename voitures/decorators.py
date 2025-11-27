from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(role_name):
    def decorator(view_func):
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role == role_name:
                return view_func(request, *args, **kwargs)
            return redirect("login")  # redirige si rôle non autorisé

        return wrapper

    return decorator
