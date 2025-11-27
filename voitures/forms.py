from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Marque,Modele,Voiture


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={
            "class": "form-control",
           
        })
    )

    email = forms.EmailField(
        label="email",
        widget=forms.EmailInput(attrs={
            "class": "form-control",
           
        })
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
         
        })
    )

    password2 = forms.CharField(
        label="Confirmer le mot de passe",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
           
        })
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

        help_texts = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }


        # Supprimer éventuellement les messages d'erreur par défaut (optionnel)
       
class CustomerLoginForm(AuthenticationForm):
    username = forms.CharField(label="Nom d'utilisateur")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    #------------marque---------------------
class MarqueForm(forms.ModelForm):
     class Meta:
        model = Marque
        fields = ['nom']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la marque'}),
          
        }
    #-------------modele---------------------------------
class ModeleForm(forms.ModelForm):
    class Meta:
        model = Modele
        fields = ["nom", "marque"]
        widgets = {
            "nom": forms.TextInput(attrs={"class": "form-control",'placeholder':"nom du modele/voiture"}),
           
        }
    #-------------------gestion voiture-----------------------------------

class VoitureForm(forms.ModelForm):
    class Meta:
        model = Voiture
        fields = [
            'marque', 'modele', 'numero_chassis', 'numero_moteur',
            'annee', 'transmission', 'kilometrage', 'couleur',
            'cylindree_cc', 'prix', 'photo', 'etat'
        ]
        widgets = {
            'marque': forms.Select(attrs={'class': 'form-control'}),
            'modele': forms.Select(attrs={'class': 'form-control'}),
            'numero_chassis': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_moteur': forms.TextInput(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'transmission': forms.Select(attrs={'class': 'form-control'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control'}),
            'couleur': forms.TextInput(attrs={'class': 'form-control'}),
            'cylindree_cc': forms.NumberInput(attrs={'class': 'form-control'}),
            'prix': forms.NumberInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
        }


        
          
    
        