import re
from django.core.exceptions import ValidationError


def validate_strong_password(password):
    """
    Vérifie que le mot de passe contient :
    - au moins 1 majuscule
    - au moins 1 minuscule
    - au moins 1 chiffre
    - au moins 1 symbole
    """

    if len(password) < 8:
        raise ValidationError(
            "Le mot de passe doit contenir au moins 8 caractères."
        )

    if not re.search(r"[A-Z]", password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins une lettre majuscule."
        )

    if not re.search(r"[a-z]", password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins une lettre minuscule."
        )

    if not re.search(r"[0-9]", password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins un chiffre."
        )

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError(
            "Le mot de passe doit contenir au moins un symbole."
        )
