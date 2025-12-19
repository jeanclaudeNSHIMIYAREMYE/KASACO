from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Marque, Modele, Voiture, Reservation
from .validators import validate_strong_password,validate_voiture_form

# ----------------- User Forms -----------------
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                "placeholder": "Nom d'utilisateur",
            }
        ),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                "placeholder": "Email",
            }
        ),
    )
    password1 = forms.CharField(
        label="Mot de passe",
        validators=[validate_strong_password],
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                "placeholder": "Mot de passe",
            }
        ),
    )
    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                "placeholder": "Confirmer le mot de passe",
            }
        ),
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]
        help_texts = {field: "" for field in fields}


    def clean_username(self):
        username=self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError(
                "Cette nom d'utilisateur est déjà utilisée."

            )
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Cette adresse email est déjà utilisée.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise ValidationError("Les mots de passe ne correspondent pas.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomerLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 "
                         "focus:ring-2 focus:ring-red-500 focus:border-red-500 transition",
                "placeholder": "exemple@gmail.com",
            }
        ),
    )

    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(
            attrs={
                "class": "w-full border border-gray-300 rounded-lg px-4 py-2 "
                         "focus:ring-2 focus:ring-red-500 focus:border-red-500 transition",
                "placeholder": "Votre mot de passe",
            }
        ),
    )


# ----------------- Marque Form -----------------
class MarqueForm(forms.ModelForm):
    class Meta:
        model = Marque
        fields = ["nom", "logo"]
        widgets = {
            "nom": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                       "placeholder": "Nom de la marque"}
            ),
            "logo": forms.ClearableFileInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-red-500"}
            ),
        }


# ----------------- Modele Form -----------------
class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = ["nom", "marque"]
        widgets = {
            "nom": forms.TextInput(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500",
                       "placeholder": "Nom du modèle"}
            ),
            "marque": forms.Select(
                attrs={"class": "w-full border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-red-500"}
            ),
        }


# ----------------- Voiture Form -----------------
class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = [
            "marque", "modele", "numero_chassis", "numero_moteur",
            "annee", "transmission", "kilometrage", "couleur",
            "cylindree_cc", "prix", "photo", "etat",
        ]

        widgets = {
            "marque": forms.Select(attrs={
                "class": "w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
            }),
            "modele": forms.Select(attrs={
                "class": "w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
            }),
            "transmission": forms.Select(attrs={
                "class": "w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
            }),
            "etat": forms.Select(attrs={
                "class": "w-full px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
            }),
            "numero_chassis": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "numero_moteur": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "couleur": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "annee": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "kilometrage": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "cylindree_cc": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "prix": forms.NumberInput(attrs={
                "class": "w-full px-4 py-2 bg-gray-100 border border-gray-300 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500"
            }),
            "photo": forms.FileInput(attrs={
                "class": "w-full text-gray-700 bg-white border border-gray-300 rounded-lg cursor-pointer "
                         "file:bg-blue-600 file:text-white file:px-4 file:py-2 file:rounded-md "
                         "file:border-none hover:file:bg-blue-700 shadow-sm"
            }),
        }

         # Validation champ spécifique
    def clean_numero_chassis(self):
        numero_chassis = self.cleaned_data.get('numero_chassis')
        if Voiture.objects.filter(numero_chassis=numero_chassis).exists():
            raise forms.ValidationError("Ce numéro de châssis est déjà utilisé.")
        return numero_chassis

    # Validation globale via validators.py
    def clean(self):
        cleaned_data = super().clean()
        try:
            validate_voiture_form(cleaned_data)  # Appel de ton validator global
        except forms.ValidationError as e:
            raise forms.ValidationError(e)
        return cleaned_data


# ----------------- Multiple images -----------------
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs.update({
            "multiple": True,
            "accept": "image/*",
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg bg-white cursor-pointer shadow-sm "
                     "file:bg-green-600 file:text-white file:border-none file:px-4 file:py-2 file:rounded-lg "
                     "hover:file:bg-green-700 focus:ring-2 focus:ring-green-500"
        })
        super().__init__(attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        if isinstance(data, (list, tuple)):
            return [super(MultipleFileField, self).clean(d, initial) for d in data]
        return super().clean(data, initial)


class ImageForm(forms.Form):
    images = MultipleFileField(label="Télécharger plusieurs images", required=False)


# ----------------- Reservation Form -----------------
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["utilisateur"]
        widgets = {
            "utilisateur": forms.Select(
                attrs={
                    "class": (
                        "block w-full px-4 py-2 border border-gray-300 rounded-lg "
                        "bg-white text-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 "
                        "focus:border-blue-500"
                    )
                }
            ),
        }
        labels = {
            "utilisateur": "Sélectionnez l'utilisateur",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["utilisateur"].queryset = CustomUser.objects.all()
        self.fields["utilisateur"].label_from_instance = lambda obj: obj.username
