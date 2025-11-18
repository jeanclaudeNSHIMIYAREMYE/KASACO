from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomerLoginForm, MarqueForm, ModeleForm, VoitureForm
from .decorators import role_required
from .models import CustomUser, Marque, Modele, Voiture

# Page d'accueil
def home(request):
    return render(request, 'voiture/base.html')

# Inscription
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("redirect_by_role")
        else:
            messages.error(request, "Erreur lors de l'inscription, veuillez vérifier le formulaire.")
    else:
        form = CustomUserCreationForm()
    return render(request, "voiture/auth/signup.html", {"form": form})

# Connexion
def login_view(request):
    if request.method == "POST":
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect("redirect_by_role")
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    else:
        form = CustomerLoginForm()
    return render(request, "voiture/auth/login.html", {"form": form})

# Déconnexion
def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect("home")

# Redirection automatique selon rôle
def redirect_by_role(request):
    if request.user.role == "admin":
        return redirect("dashboard_admin")
    return redirect("user_home")

# Dashboard administrateur
@role_required("admin")
def admin_dashboard(request):
    messages.success(request, "Bienvenue sur le dashboard admin !")
    return render(request, "voiture/admin/dashboard.html")

# Dashboard utilisateur
@role_required("user")
def user_home(request):
    voitures = Voiture.objects.all().order_by('-date_ajout')
    return render(request, "voiture/user/index.html", {'voitures': voitures})

# ------------------- Gestion utilisateurs -------------------
@role_required("admin")
def utilisateurs_list(request):
    users = CustomUser.objects.all()
    return render(request, 'voiture/admin/users.html', {'users': users})

@role_required("admin")
def supprimer_utilisateur(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user != user:  # éviter que l’admin supprime lui-même
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
    else:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
    return redirect('utilisateurs_list')

@role_required("admin")
def changer_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if user.role == 'admin':
        user.role = 'user'
    else:
        user.role = 'admin'
    user.save()
    messages.success(request, f"Le rôle de {user.username} a été changé avec succès.")
    return redirect('utilisateurs_list')

# ------------------- Gestion marques -------------------
@role_required("admin")
def liste_marques(request):
    marques = Marque.objects.all()
    form = MarqueForm()
    return render(request, 'voiture/admin/marque.html', {"marques": marques, "form": form})

@role_required("admin")
def ajouter_marque(request):
    if request.method == "POST":
        form = MarqueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Marque ajoutée avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout de la marque.")
    return redirect('liste_marques')

@role_required("admin")
def supprimer_marque(request, id):
    marque = get_object_or_404(Marque, id=id)
    marque.delete()
    messages.success(request, "Marque supprimée avec succès !")
    return redirect("liste_marques")

# ------------------- Gestion modèles -------------------
@role_required("admin")
def liste_modeles(request):
    modeles = Modele.objects.select_related("marque").all().order_by("-id")
    form = ModeleForm()
    return render(request, "voiture/admin/modele.html", {"modeles": modeles, "form": form})

@role_required("admin")
def ajouter_modele(request):
    if request.method == "POST":
        form = ModeleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Modèle ajouté avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout du modèle.")
    return redirect("liste_modeles")

@role_required("admin")
def supprimer_modele(request, id):
    modele = get_object_or_404(Modele, id=id)
    modele.delete()
    messages.success(request, "Modèle supprimé avec succès !")
    return redirect("liste_modeles")

# ------------------- Gestion voitures -------------------
@role_required("admin")
def liste_voitures(request):
    voitures = Voiture.objects.all()
    form = VoitureForm()
    return render(request, 'voiture/admin/voiture.html', {'voitures': voitures, 'form': form})

@role_required("admin")
def ajouter_voiture(request):
    if request.method == "POST":
        form = VoitureForm(request.POST, request.FILES)
        if form.is_valid():
            voiture = form.save()
            messages.success(request, f'La voiture {voiture} a été ajoutée avec succès.')
        else:
            messages.error(request, "Erreur lors de l'ajout de la voiture.")
    return redirect('liste_voitures')

@role_required("admin")
def supprimer_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    voiture.delete()
    messages.success(request, f'La voiture {voiture} a été supprimée avec succès.')
    return redirect('liste_voitures')
