import re
from django.core.exceptions import ValidationError
from datetime import datetime

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
def validate_voiture_form(cleaned_data):
    """
    validation global pour le formulaire
   """
    errors={}

#recuperer les champs
    prix = cleaned_data.get('prix')
    kilometrage =cleaned_data.get('kilometrage')
    annee= cleaned_data.get('annee')
    cylindree_cc=cleaned_data.get('cylindree_cc')

    #validation de prix
    if prix is not None and prix <= 0 :
        errors['prix']="Le prix doit être supérieur à zéro."
        #validation de kilometrage
    if kilometrage is not None and kilometrage < 0:
        errors['kilometrage']='Le kilométrage ne peut pas être négatif.'
    #validation annee
    current_year = datetime.now().year
    if annee is not None and (annee < 1900 or annee > current_year):
        errors["annee"] = f"L'année doit être entre 1900 et {current_year}."
        #validation cylindree_cc

    if cylindree_cc is not None and cylindree_cc <= 0:
        errors["cylindree_cc"] = "La cylindrée doit être supérieure à zéro."

         # Si des erreurs ont été collectées, lever ValidationError
    if errors:
        raise ValidationError(errors)
