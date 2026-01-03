from functools import wraps

from django.contrib import messages
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


def admin_required(view_func):
    """
    Autorise uniquement les utilisateurs admin (staff ou superuser)
    """

    @login_required
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):

        if request.user.is_staff or request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        messages.error(request, "Accès refusé : réservé à l'administrateur.")
        return redirect("liste_voitures")

    return _wrapped_view
