from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser,Marque,Modele,Voiture


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "password1", "password2"]

        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"} ),
            "email": forms.EmailInput(attrs={ "class": "form-control","placeholder": "Adresse email" }),
            "password1": forms.PasswordInput(attrs={ "class": "form-control","placeholder": "Mot de passe" } ),
            "password2": forms.PasswordInput( attrs={ "class": "form-control", "placeholder": "Confirmer le mot de passe"}),
        }

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
            'cylindree_cc', 'prix', 'image', 'etat'
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
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'etat': forms.Select(attrs={'class': 'form-control'}),
        }


        
          
    
        