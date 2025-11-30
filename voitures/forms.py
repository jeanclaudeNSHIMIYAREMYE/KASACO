from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser, Marque, Modele, Voiture


# ----------------- User -----------------
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                "placeholder": "Email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                "placeholder": "Mot de passe",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                "placeholder": "Confirmer le mot de passe",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        help_texts = {field: "" for field in fields}


# ----------------- Login -----------------
class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            }
        ),
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
            }
        ),
    )


# ----------------- Marque -----------------
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = ["nom"]
        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                    "placeholder": "Nom de la marque",
                }
            ),
        }


# ----------------- Modele -----------------
class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = ["nom", "marque"]
        widgets = {
            "nom": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500",
                    "placeholder": "Nom du modèle/voiture",
                }
            ),
            "marque": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500"
                }
            ),
        }


# ----------------- Voiture -----------------
class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = [
            "marque",
            "modele",
            "numero_chassis",
            "numero_moteur",
            "annee",
            "transmission",
            "kilometrage",
            "couleur",
            "cylindree_cc",
            "prix",
            "photo",
            "etat",
        ]
        widgets = {
            "marque": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-red-500"
                }
            ),
            "modele": forms.Select(
                attrs={
                    "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500 focus:border-red-500"
                }
            ),
            "numero_chassis": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "numero_moteur": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "annee": forms.NumberInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "transmission": forms.Select(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "kilometrage": forms.NumberInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "couleur": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "cylindree_cc": forms.NumberInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "prix": forms.NumberInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "w-full text-gray-700"}),
            "etat": forms.Select(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2"}
            ),
        }
