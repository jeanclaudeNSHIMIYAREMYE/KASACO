from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.core.mail import send_mail
from .decorators import role_required
from .forms import (CustomerLoginForm, CustomUserCreationForm, MarqueForm,
                    ModeleForm, VoitureForm ,ImageForm , ReservationForm)
from .models import (ContactInfo, CustomUser, Marque, Modele,
                     Reservation, Voiture ,Image)
from django.core.mail import send_mail
import os
from django.conf import settings


# ----------------- Page d'accueil -----------------


def home(request):
    voitures = Voiture.objects.all().order_by('-date_ajout')
    marques = Marque.objects.prefetch_related('modeles')
    modeles = Modele.objects.prefetch_related('voitures')[:4]
    voitures_populaires = Voiture.objects.order_by('-date_ajout')[:6]  # 10 dernières voitures

    # --- RECHERCHE ---
    query = request.GET.get('q')
    if query:
        voitures = voitures.filter(
            Q(modele__nom__icontains=query) |
            Q(marque__nom__icontains=query) |
            Q(numero_chassis__icontains=query) |
            Q(numero_moteur__icontains=query) |
            Q(couleur__icontains=query) |
            Q(annee__icontains=query) |
            Q(transmission__icontains=query) |
            Q(cylindree_cc__icontains=query) |
            Q(prix__icontains=query)
        )

    # --- Message si aucun résultat ---
    message = None
    if not voitures.exists():
        message = "Aucune voiture trouvée pour votre recherche."

    # --- Pagination ---
    paginator = Paginator(voitures, 3)  # 6 voitures par page
    page_number = request.GET.get('page')
    voitures_page = paginator.get_page(page_number)

    context = {
        'voitures': voitures_page,
        'marques': marques,
        'modeles': modeles,
        'voitures_populaires': voitures_populaires,
        'message': message,
    }
    return render(request, 'voiture/main.html', context)









# voiture/views.py
from django.shortcuts import render

def pourquoi_kasaco(request):
    """
    Page expliquant pourquoi choisir KASACO.
    """
    context = {
        'title': "Pourquoi KASACO ?",
        'features': [
            {
                'icon': 'bi bi-building text-red-500',
                'title': 'Vente et importation des véhicules locales',
                'description': 'Nous proposons un large choix de véhicules locaux de qualité soigneusement inspectés et certifiés.',
            },
            {
                'icon': 'bi bi-globe2 text-blue-500',
                'title': 'Vente et importation des véhicules en ligne',
                'description': 'Achetez facilement votre véhicule en ligne avec livraison rapide et sécurisée partout au Burundi.',
            },
            {
                'icon': 'bi bi-car-front-fill text-green-500',
                'title': 'Garage',
                'description': 'Nos garages sont équipés pour l’entretien, la réparation et le service après-vente de votre véhicule.',
            },
        ]
    }
    return render(request, 'voiture/pourquoi_kasaco.html', context)





# ----------------- Inscription -----------------
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("redirect_by_role")
        else:
            messages.error(
                request,
                "Erreur lors de l'inscription, veuillez vérifier le formulaire.",
            )
    else:
        form = CustomUserCreationForm()
    return render(request, "voiture/auth/signup.html", {"form": form})


# ----------------- Connexion -----------------
def login_view(request):
    if request.method == "POST":
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Connexion réussie !")
            return redirect("redirect_by_role")
        else:
            messages.error(request, "email ou mot de passe incorrect.")
    else:
        form = CustomerLoginForm()
    return render(request, "voiture/auth/login.html", {"form": form})


# ----------------- Déconnexion -----------------
def logout_view(request):
    logout(request)
    return redirect("home")


# ----------------- Redirection selon rôle -----------------
def redirect_by_role(request):
    if request.user.role == "admin":
        return redirect("dashboard_admin")
    return redirect("user_home")


# ----------------- Dashboard administrateur -----------------
@role_required("admin")
def admin_dashboard(request):
    stats = {
        "utilisateurs_count": CustomUser.objects.count(),
        "voitures_count": Voiture.objects.count(),
        "reservations_count": Reservation.objects.count(),
        "marques_count": Marque.objects.count(),
    }
    return render(request, "voiture/admin/dashboard.html", stats)


# ----------------- Dashboard utilisateur -----------------
@role_required("user")
def user_home(request):
    item_name = request.GET.get("item_name")
    voitures = Voiture.objects.all().order_by("-date_ajout")

    if item_name:
        voitures = voitures.filter(
            Q(modele__nom__icontains=item_name)
            | Q(marque__nom__icontains=item_name)
            | Q(numero_chassis__icontains=item_name)
        )

    message = None
    if not voitures.exists():
        message = "Aucune voiture trouvée pour votre recherche."

    paginator = Paginator(voitures, 4)  # 4 voitures par page
    page = request.GET.get("page")
    voitures = paginator.get_page(page)

    return render(
        request,
        "voiture/user/index.html",
        {"voitures": voitures, "item_name": item_name, "message": message},
    )


@role_required("user")
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)

    if voiture.etat == "Disponible":
        Reservation.objects.create(utilisateur=request.user, voiture=voiture)
        voiture.reserver()  # Assurez-vous que la méthode 'reserver' existe dans le modèle Voiture
        messages.success(
            request,
            f"Vous avez réservé la voiture {voiture.marque.nom} {voiture.modele.nom} avec succès !",
        )
    else:
        messages.warning(request, "Cette voiture est déjà réservée.")
    return redirect("user_home")


# ----------------- Liste des réservations -----------------
@role_required("user")
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)

    if voiture.etat == "Disponible":
        Reservation.objects.create(utilisateur=request.user, voiture=voiture)
        voiture.reserver()  # Assurez-vous que la méthode 'reserver' existe dans le modèle Voiture
        messages.success(
            request,
            f"Vous avez réservé la voiture {voiture.marque.nom} {voiture.modele.nom} avec succès !",
        )
    else:
        messages.warning(request, "Cette voiture est déjà réservée.")
    return redirect("user_home")


# ----------------- Liste des réservations -----------------


@role_required("admin")
def reserver(request):
    # Récupérer toutes les réservations avec info voiture et utilisateur
    voitures_reservees = Reservation.objects.select_related(
        'voiture', 'utilisateur', 'voiture__marque', 'voiture__modele'
    ).all().order_by('-date_reservation')

    # Statistiques
    total_voitures = Voiture.objects.count()
    total_reservees = Reservation.objects.count()
    total_utilisateurs = CustomUser.objects.count()

    # Pagination (10 réservations par page)
    paginator = Paginator(voitures_reservees, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "voitures_reservees": page_obj,  # Pour itérer dans le template
        "total_voitures": total_voitures,
        "total_reservees": total_reservees,
        "total_utilisateurs": total_utilisateurs,
    }

    return render(request, "voiture/admin/reserver.html", context)



# ----------------- Détails d'une voiture -----------------
def detail(request, myid):
    voiture = get_object_or_404(Voiture, id=myid)
    images_supp = Image.objects.filter(voiture=voiture)

    return render(
        request,
        "voiture/user/details.html",
        {
            "voiture": voiture,
            "images_supp": images_supp,
        }
    )

# ----------------- Gestion utilisateurs -----------------
@role_required("admin")
def utilisateurs_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')  # Les plus récents d'abord
    paginator = Paginator(users, 5)  # 5 utilisateurs par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "voiture/admin/users.html", {
        'page_obj': page_obj,
    })
@role_required("admin")
def supprimer_utilisateur(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user != user:
        user.delete()
        messages.success(request, "Utilisateur supprimé avec succès.")
    else:
        messages.error(request, "Vous ne pouvez pas supprimer votre propre compte.")
    return redirect("utilisateurs_list")


@role_required("admin")
def changer_role(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.role = "user" if user.role == "admin" else "admin"
    user.save()
    messages.success(request, f"Le rôle de {user.username} a été changé avec succès.")
    return redirect("utilisateurs_list")


# ----------------- Gestion marques -----------------


@role_required("admin")
def liste_marques(request):
    marques_list = Marque.objects.all().order_by("nom")
    paginator = Paginator(marques_list, 5)  # 5 marques par page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    form = MarqueForm()

    return render(
        request,
        "voiture/admin/marque.html",
        {
            "page_obj": page_obj,
            "form": form,
        },
    )




@role_required("admin")
def add_mark(request):
    if request.method == "POST":
        # On passe request.POST et request.FILES pour gérer l'upload
        form = MarqueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Marque ajoutée avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout de la marque.")
    return redirect("liste_marques")


@role_required("admin")
def supprimer_marque(request, id):
    marque = get_object_or_404(Marque, id=id)
    marque.delete()
    messages.success(request, "Marque supprimée avec succès !")
    return redirect("liste_marques")


# ----------------- Gestion modèles -----------------
@role_required("admin")
def liste_modeles(request):
    modeles = Modele.objects.select_related("marque").all().order_by("-id")

    # Pagination : 10 éléments par page
    paginator = Paginator(modeles, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    form = ModeleForm()

    return render(
        request,
        "voiture/admin/modele.html",
        {"page_obj": page_obj, "form": form}
    )


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


# ----------------- Gestion voitures -----------------
@role_required("admin")
def liste_voitures(request):
    voitures = Voiture.objects.all()
    paginator = Paginator(voitures, 5)   # 10 véhicules par page
    page = request.GET.get("page")
    voitures = paginator.get_page(page)
    form = VoitureForm()
    return render(
        request, "voiture/admin/voiture.html", {"voitures": voitures, "form": form}
    )

@role_required("admin")
def ajouter_voiture(request):
    if request.method == "POST":
        v_form = VoitureForm(request.POST, request.FILES)
        img_form = ImageForm(request.POST, request.FILES)

        if v_form.is_valid() and img_form.is_valid():
            voiture = v_form.save(commit=False)
            voiture.save()

            # Enregistrer chaque image uploadée
            images = request.FILES.getlist("images")
            for f in images:
                Image.objects.create(voiture=voiture, image=f)

            messages.success(
                request,
                f"La voiture {voiture.marque.nom} {voiture.modele.nom} a été publiée avec succès."
            )
            return redirect("liste_voitures")
        else:
            messages.error(request, "Erreur lors de la publication de la voiture.")

    else:
        v_form = VoitureForm()
        img_form = ImageForm()

    context = {
        "v_form": v_form,
        "img_form": img_form,
    }
    return render(request, "voiture/admin/ajouter_voiture.html", context)





@role_required("admin")
def supprimer_voiture(request, id):
    voiture = get_object_or_404(Voiture, id=id)
    voiture.delete()
    messages.success(request, f"La voiture {voiture} a été supprimée avec succès.")
    return redirect("liste_voitures")


def info(request):
    contact_info = ContactInfo.objects.first()  # récupère le premier enregistrement
    return render(request, "voiture/info.html", {"contact_info": contact_info})


# --- Vue pour afficher contact seul (optionnel) ---
def contact_view(request):
    contact_info = ContactInfo.objects.first()
    return render(request, "voiture/contact.html", {"contact_info": contact_info})


@role_required("user")
def mes_reservations(request):
    """
    Affiche les réservations de l'utilisateur connecté
    """
    reservations = Reservation.objects.select_related('voiture').filter(
        utilisateur=request.user
    ).order_by('-date_reservation')

    context = {
        "reservations": reservations
    }

    return render(request, "voiture/user/mes_reservations.html", context)




@staff_member_required
def disponible_liste_voitures(request):
    voitures_list = Voiture.objects.filter(etat="Disponible").order_by('-id')  # ordonner par ID décroissant

    # Pagination
    paginator = Paginator(voitures_list, 5)  # 10 voitures par page
    page_number = request.GET.get('page')
    voitures = paginator.get_page(page_number)

    reservations = Reservation.objects.select_related('voiture', 'utilisateur').all().order_by('-date_reservation')

    context = {
        "voitures": voitures,
        "reservations": reservations
    }

    return render(request, "voiture/admin/disponible_liste_voiture.html", context)



@staff_member_required
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)

    if voiture.etat != "Disponible":
        messages.error(request, "Cette voiture n'est plus disponible.")
        return redirect("reserver_liste_voitures")

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.voiture = voiture
            reservation.save()

            # Mettre la voiture en état réservé
            voiture.reserver()

            # =========================
            # 📧 ENVOI EMAIL
            # =========================
            sujet = "Confirmation de réservation - KASACO 🚗"

            message = f"""
Bonjour {reservation.utilisateur.username},

Votre réservation a été effectuée avec succès.

📌 Détails de la réservation :
- Voiture : {voiture}
- Prix : {voiture.prix} $
- Date : {reservation.date_reservation.strftime('%d/%m/%Y %H:%M')}

Merci de faire confiance à KASACO.

Cordialement,
L’équipe KASACO 🚀
"""

            destinataire = [reservation.utilisateur.email]

            # Lecture sûre du DEFAULT_FROM_EMAIL depuis l'environnement
            from_email = os.environ.get("DEFAULT_FROM_EMAIL", settings.DEFAULT_FROM_EMAIL)

            try:
                send_mail(
                    subject=sujet,
                    message=message,
                    from_email=from_email,
                    recipient_list=destinataire,
                    fail_silently=False,
                )
                messages.success(request, "Voiture réservée avec succès. Un email de confirmation a été envoyé.")
            except Exception as e:
                messages.warning(request, f"Voiture réservée mais l'email n'a pas pu être envoyé : {e}")

            return redirect("liste_voitures")
    else:
        form = ReservationForm()

    return render(
        request,
        "voiture/admin/reserver.html",
        {
            "voiture": voiture,
            "form": form,
        },
    )

