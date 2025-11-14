from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomerLoginForm
from .decorators import role_required

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
            return redirect("redirect_by_role")
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
            return redirect("redirect_by_role")
    else:
        form = CustomerLoginForm()
    return render(request, "voiture/auth/login.html", {"form": form})


# Déconnexion
def logout_view(request):
    logout(request)
    return redirect("home")


# Redirection automatique selon rôle
def redirect_by_role(request):
    if request.user.role == "admin":
        return redirect("dashboard_admin")
    return redirect("user_home")


# Dashboard administrateur (protégé par rôle)
@role_required("admin")
def admin_dashboard(request):
    return render(request, "voiture/admin/dashboard.html")


# Dashboard utilisateur (protégé par rôle)
@role_required("user")
def user_home(request):
    return render(request, "voiture/user/home.html")
