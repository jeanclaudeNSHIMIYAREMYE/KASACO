from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomerLoginForm, MarqueForm, ModeleForm, VoitureForm
from .decorators import role_required
from django.db.models import Q
from django.core.paginator import Paginator

from .models import CustomUser, Marque, Modele, Voiture , Commande,Reservation

# Page d'accueil
def home(request):
  return render(request, 'voiture/main.html')

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
    
    stats = {
        'utilisateurs_count': CustomUser.objects.count(),
        'voitures_count': Voiture.objects.count(),
        'reservations_count': Reservation.objects.count(),
        'marques_count': Marque.objects.count(),
    }
    messages.success(request, "Bienvenue sur le dashboard admin !")
    return render(request, "voiture/admin/dashboard.html", stats)

# Dashboard utilisateur



role_required("user")
def user_home(request):
    # Terme recherché
    item_name = request.GET.get('item_name')

    # Base queryset
    voitures = Voiture.objects.all().order_by('-date_ajout')

    # Si une recherche est faite
    if item_name:
        voitures = voitures.filter(
            Q(modele__nom__icontains=item_name) |
            Q(marque__nom__icontains=item_name) |
            Q(numero_chassis__icontains=item_name)
        )

    # Vérifier si aucune voiture n’est trouvée
    if not voitures.exists():
        message = "Aucune voiture trouvée pour votre recherche."
    else:
        message = None

    # Pagination
    paginator = Paginator(voitures, 4)  # 4 voitures par page
    page = request.GET.get('page')
    voitures = paginator.get_page(page)

    return render(request, "voiture/user/index.html", {
        'voitures': voitures,
        'item_name': item_name,
        'message': message
    })
@role_required("user")
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    
    if voiture.etat == 'Disponible':
        # Créer la réservation
        Reservation.objects.create(utilisateur=request.user, voiture=voiture)
        # Mettre à jour l'état de la voiture
        voiture.reserver()
        # Message de confirmation
        messages.success(request, f"Vous avez réservé la voiture {voiture.marque.nom} {voiture.modele.nom} avec succès !")
    else:
        messages.warning(request, "Cette voiture est déjà réservée.")

    return redirect('user_home')


def reserver(request):
    total_voitures = Voiture.objects.count()
    total_reservees = Voiture.objects.filter(etat='Réservée').count()
    total_utilisateurs = CustomUser.objects.filter(role='user').count()

    # Liste des voitures réservées avec leur utilisateur
    voitures_reservees = Reservation.objects.select_related('voiture', 'utilisateur').all()

    context = {
        'total_voitures': total_voitures,
        'total_reservees': total_reservees,
        'total_utilisateurs': total_utilisateurs,
        'voitures_reservees': voitures_reservees,
    }
    return render(request, 'voiture/admin/reserver.html', context)
    
    
    
    
    
    
    
    
    
    
    
    #----------------- details de voutures--------------
    
    
def detail(request, myid):
    voiture = get_object_or_404(Voiture, id=myid)
    return render(request, "voiture/user/details.html", {"voiture": voiture})






def checkout(request):
    if request.method=="POST":
        items=request.POST.get('items')
        total=request.POST.get('total')
        nom=request.POST.get('nom')
        email=request.POST.get('email')
        address=request.POST.get('address')
        ville=request.POST.get('ville')
        pays=request.POST.get('pays')
        zipcode=request.POST.get('zipcode')
        com=Commande(items=items,total=total,nom=nom,email=email,address=address,ville=ville,pays=pays,zipcode=zipcode)
        com.save()
    
    return render(request, 'voiture/user/checkout.html')




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
            messages.success(request, f'La voiture {voiture} a été publie avec succès.')
        else:
            messages.error(request, "Erreur lors de publication de la voiture.")
    return redirect('liste_voitures')

@role_required("admin")
def supprimer_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    voiture.delete()
    messages.success(request, f'La voiture {voiture} a été supprimée avec succès.')
    return redirect('liste_voitures')



