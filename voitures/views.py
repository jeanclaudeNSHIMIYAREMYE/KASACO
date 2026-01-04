import os
import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .decorators import role_required
from .forms import (
    CustomerLoginForm,
    CustomUserCreationForm,
    ImageForm,
    MarqueForm,
    ModeleForm,
    ReservationForm,
    VoitureForm,
)
from .models import ContactInfo, CustomUser, Image, Marque, Modele, Reservation, Voiture

# ----------------- Page d'accueil -----------------


def home(request):
    voitures = Voiture.objects.all().order_by("-date_ajout")
    marques = Marque.objects.prefetch_related("modeles")
    modeles = Modele.objects.prefetch_related("voitures")[:4]
    voitures_populaires = Voiture.objects.order_by("-date_ajout")[
        :6
    ]  # 10 dernières voitures

    # --- RECHERCHE ---
    query = request.GET.get("q")
    if query:
        voitures = voitures.filter(
            Q(modele__nom__icontains=query)
            | Q(marque__nom__icontains=query)
            | Q(numero_chassis__icontains=query)
            | Q(numero_moteur__icontains=query)
            | Q(couleur__icontains=query)
            | Q(annee__icontains=query)
            | Q(transmission__icontains=query)
            | Q(cylindree_cc__icontains=query)
            | Q(prix__icontains=query)
        )

    # --- Message si aucun résultat ---
    message = None
    if not voitures.exists():
        message = "Aucune voiture trouvée pour votre recherche."

    # --- Pagination ---
    paginator = Paginator(voitures, 3)  # 6 voitures par page
    page_number = request.GET.get("page")
    voitures_page = paginator.get_page(page_number)

    context = {
        "voitures": voitures_page,
        "marques": marques,
        "modeles": modeles,
        "voitures_populaires": voitures_populaires,
        "message": message,
    }
    return render(request, "voiture/main.html", context)


def pourquoi_kasaco(request):
    """
    Page expliquant pourquoi choisir KASACO.
    """
    context = {
        "title": "Pourquoi KASACO ?",
        "features": [
            {
                "icon": "bi bi-building text-red-500",
                "title": "Vente et importation des véhicules locales",
                "description": "Nous proposons un large choix de véhicules locaux de qualité soigneusement inspectés et certifiés.",
            },
            {
                "icon": "bi bi-globe2 text-blue-500",
                "title": "Vente et importation des véhicules en ligne",
                "description": "Achetez facilement votre véhicule en ligne avec livraison rapide et sécurisée partout au Burundi.",
            },
            {
                "icon": "bi bi-car-front-fill text-green-500",
                "title": "Garage",
                "description": "Nos garages sont équipés pour l’entretien, la réparation et le service après-vente de votre véhicule.",
            },
        ],
    }
    return render(request, "voiture/pourquoi_kasaco.html", context)


# ----------------- Inscription -----------------
def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
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

            return redirect("redirect_by_role")
        else:
            messages.error(request, "email ou mot de passe incorrect.")
    else:
        form = CustomerLoginForm()
    return render(request, "voiture/auth/login.html", {"form": form})


# ------------------------------------changement de mot de passe-------------------------


# Fonction pour vérifier l'email
def verification_email(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        # Vérifier que l'email est saisi
        if not email:
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return render(request, "voiture/auth/verification.html")

        # Vérifier si l'utilisateur existe
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Rediriger vers la page de changement de mot de passe en passant l'email
            return redirect("changementCode", email=email)
        else:
            messages.error(request, "Cette adresse email ne correspond à aucun compte.")
            return redirect("verification")

    return render(request, "voiture/auth/verification.html")

    # fonction de changement du mot de pass


def changementCode(request, email):
    """
    Vue pour changer le mot de passe d'un utilisateur identifié par son email.
    """
    try:
        customer = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        messages.error(request, "Utilisateur introuvable")
        return redirect("login")

    if request.method == "POST":
        # Récupération des mots de passe depuis le formulaire
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("password_confirm", "").strip()

        # Vérification de la correspondance
        if password != confirm_password:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect("changementCode", email=email)

        # Vérification de la complexité du mot de passe
        if (
            len(password) < 8
            or not re.search(r"[A-Za-z]", password)
            or not re.search(r"\d", password)
            or not re.search(r"[!@#$%^&*]", password)
        ):
            messages.error(
                request,
                "Le mot de passe doit contenir au moins 8 caractères, "
                "une lettre, un chiffre et un caractère spécial",
            )
            return redirect("changementCode", email=email)

        # Enregistrer le nouveau mot de passe
        customer.set_password(password)
        customer.save()

        messages.success(request, "Mot de passe modifié avec succès ✅")
        return redirect("login")

    # Affichage du formulaire
    return render(request, "voiture/auth/changementCode.html", {"email": email})


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
    # --- Recherche depuis le champ "q" ---
    query = request.GET.get("q", "")

    # --- Toutes les voitures triées par date d'ajout ---
    voitures = Voiture.objects.all().order_by("-date_ajout")

    # --- Filtrage si recherche ---
    if query:
        voitures = voitures.filter(
            Q(modele__nom__icontains=query)
            | Q(marque__nom__icontains=query)
            | Q(numero_chassis__icontains=query)
            | Q(numero_moteur__icontains=query)
            | Q(couleur__icontains=query)
            | Q(annee__icontains=query)
            | Q(transmission__icontains=query)
            | Q(cylindree_cc__icontains=query)
            | Q(prix__icontains=query)
        )

    # --- Message si aucun résultat ---
    message = None
    if not voitures.exists():
        message = "Aucune voiture trouvée pour votre recherche."

    # --- Pagination ---
    paginator = Paginator(voitures, 3)  # 3 voitures par page
    page_number = request.GET.get("page")
    voitures_page = paginator.get_page(page_number)

    # --- Autres données pour le template ---
    marques = Marque.objects.prefetch_related("modeles")
    modeles = Modele.objects.prefetch_related("voitures")[:4]
    voitures_populaires = Voiture.objects.order_by("-date_ajout")[:6]

    # --- Context ---
    context = {
        "voitures": voitures_page,
        "marques": marques,
        "modeles": modeles,
        "voitures_populaires": voitures_populaires,
        "item_name": query,
        "message": message,
    }

    return render(request, "voiture/user/index.html", context)


# ----------------- Liste des réservations -----------------


@role_required("admin")
def reserver(request):
    # Récupérer toutes les réservations avec info voiture et utilisateur
    voitures_reservees = (
        Reservation.objects.select_related(
            "voiture", "utilisateur", "voiture__marque", "voiture__modele"
        )
        .all()
        .order_by("-date_reservation")
    )

    # Statistiques
    total_voitures = Voiture.objects.count()
    total_reservees = Reservation.objects.count()
    total_utilisateurs = CustomUser.objects.count()

    # Pagination (10 réservations par page)
    paginator = Paginator(voitures_reservees, 10)
    page_number = request.GET.get("page")
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
@role_required("user")
def detail(request, myid):
    voiture = get_object_or_404(Voiture, id=myid)
    images_supp = Image.objects.filter(voiture=voiture)

    return render(
        request,
        "voiture/user/details.html",
        {
            "voiture": voiture,
            "images_supp": images_supp,
        },
    )


# ----------------- Gestion utilisateurs -----------------
@role_required("admin")
def utilisateurs_list(request):
    users = CustomUser.objects.all().order_by(
        "-date_joined"
    )  # Les plus récents d'abord
    paginator = Paginator(users, 5)  # 5 utilisateurs par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "voiture/admin/users.html",
        {
            "page_obj": page_obj,
        },
    )


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
        request, "voiture/admin/modele.html", {"page_obj": page_obj, "form": form}
    )


@role_required("admin")
def ajouter_modele(request):
    if request.method == "POST":
        form = ModeleForm(request.POST, request.FILES)  # <- ajouter request.FILES
        if form.is_valid():
            form.save()
            messages.success(request, "Modèle ajouté avec succès !")
        else:
            messages.error(request, "Erreur lors de l'ajout du modele.")
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
    paginator = Paginator(voitures, 5)  # 10 véhicules par page
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
                f"La voiture {voiture.marque.nom} {voiture.modele.nom} a été publiée avec succès.",
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


# fonctions pour afficher l'info du vendeur


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
    reservations = (
        Reservation.objects.select_related("voiture")
        .filter(utilisateur=request.user)
        .order_by("-date_reservation")
    )

    context = {"reservations": reservations}

    return render(request, "voiture/user/mes_reservations.html", context)


@role_required("admin")
def annuler_reservation(request, reservation_id):
    # Récupérer la réservation ou renvoyer 404
    reservation = get_object_or_404(Reservation, id=reservation_id)

    # Changer l'état de la voiture en "Disponible"
    voiture = reservation.voiture
    voiture.etat = "Disponible"
    voiture.save()

    # Supprimer la réservation
    reservation.delete()

    # Message de succès
    messages.success(
        request,
        f"La réservation de {voiture.marque.nom} {voiture.modele.nom} a été annulée.",
    )

    # Rediriger vers la page des réservations
    return redirect("liste_voitures")


@role_required("admin")
def disponible_liste_voitures(request):
    voitures_list = Voiture.objects.filter(etat="Disponible").order_by("-id")
    # ordonner par ID décroissant

    # Pagination
    paginator = Paginator(voitures_list, 5)  # 10 voitures par page
    page_number = request.GET.get("page")
    voitures = paginator.get_page(page_number)

    reservations = (
        Reservation.objects.select_related("voiture", "utilisateur")
        .all()
        .order_by("-date_reservation")
    )

    context = {"voitures": voitures, "reservations": reservations}

    return render(request, "voiture/admin/disponible_liste_voiture.html", context)


# views.py


@role_required("admin")
def reserver_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)

    if voiture.etat != "Disponible":
        messages.error(request, "Cette voiture n'est plus disponible.")
        return redirect("liste_voitures")

    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    reservation = form.save(commit=False)
                    reservation.voiture = voiture
                    reservation.save()

                    # Mettre la voiture en réservé
                    voiture.reserver()

                # Envoi email
                if reservation.utilisateur.email:
                    sujet = "Confirmation de réservation - KASACO 🚗"
                    message = f"""
Bonjour {reservation.utilisateur.username},

Votre réservation a été effectuée avec succès.

Détails de la réservation :
- Voiture : {voiture}
- Prix : {voiture.prix} $
- Date : {reservation.date_reservation.strftime('%d/%m/%Y %H:%M')}

Merci de faire confiance à KASACO.

Cordialement,
L’équipe KASACO 🚀
"""
                    from_email = os.environ.get(
                        "DEFAULT_FROM_EMAIL", settings.DEFAULT_FROM_EMAIL
                    )
                    try:
                        send_mail(
                            sujet, message, from_email, [reservation.utilisateur.email]
                        )
                        messages.success(
                            request, "Voiture réservée et email envoyé avec succès."
                        )
                    except Exception:
                        messages.warning(
                            request,
                            "Voiture réservée, mais l'email n'a pas pu être envoyé.",
                        )
                else:
                    messages.warning(
                        request,
                        "Voiture réservée, mais l'utilisateur n'a pas d'adresse email.",
                    )

                return redirect("liste_voitures")

            except Exception:
                messages.error(
                    request, "Une erreur est survenue lors de la réservation."
                )
    else:
        form = ReservationForm()

    return render(
        request, "voiture/admin/reserver.html", {"voiture": voiture, "form": form}
    )


# partie principale du client pour parcours des pages


def marque_list(request):
    marques = Marque.objects.all()
    return render(request, "voiture/marque_list.html", {"marques": marques})


def modele_list(request, marque_id):
    marque = get_object_or_404(Marque, id=marque_id)
    modeles = marque.modeles.all()

    return render(
        request, "voiture/modele_list.html", {"marque": marque, "modeles": modeles}
    )


def modele_search(request, modele_id):
    modele = get_object_or_404(Modele, id=modele_id)

    voitures = Voiture.objects.filter(modele=modele, etat="Disponible")

    # FILTRES
    annee_min = request.GET.get("annee_min")
    annee_max = request.GET.get("annee_max")
    prix_min = request.GET.get("prix_min")
    prix_max = request.GET.get("prix_max")
    transmission = request.GET.get("transmission")

    if annee_min:
        voitures = voitures.filter(annee__gte=annee_min)
    if annee_max:
        voitures = voitures.filter(annee__lte=annee_max)
    if prix_min:
        voitures = voitures.filter(prix__gte=prix_min)
    if prix_max:
        voitures = voitures.filter(prix__lte=prix_max)
    if transmission:
        voitures = voitures.filter(transmission=transmission)

    return render(
        request, "voiture/modele_search.html", {"modele": modele, "voitures": voitures}
    )


# datails du vouture pour acceuil


def voiture_detail(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)

    # Récupérer les images supplémentaires liées à cette voiture
    images_supp = Image.objects.filter(voiture=voiture)

    return render(
        request,
        "voiture/voiture_detail.html",
        {"voiture": voiture, "images_supp": images_supp},
    )


# Assurez-vous que votre décorateur est bien importé user


# ---------------------------
# LISTE DES MARQUES
# ---------------------------
@role_required("user")
def marque_auth(request):
    marques = Marque.objects.all()
    return render(request, "voiture/user/marque_auth.html", {"marques": marques})


# ---------------------------
# LISTE DES MODÈLES D'UNE MARQUE
# ---------------------------
@role_required("user")
def modele_auth(request, marque_id):
    marque = get_object_or_404(Marque, id=marque_id)
    modeles = (
        marque.modeles.all()
    )  # suppose que vous avez une relation related_name='modeles'
    return render(
        request, "voiture/user/modele_auth.html", {"marque": marque, "modeles": modeles}
    )


# ---------------------------
# RECHERCHE PAR MODÈLE AVEC FILTRES USER
# ---------------------------
@role_required("user")
def modele_search_auth(request, modele_id):
    modele = get_object_or_404(Modele, id=modele_id)
    voitures = Voiture.objects.filter(modele=modele, etat="Disponible")

    # --- FILTRES ---
    annee_min = request.GET.get("annee_min")
    annee_max = request.GET.get("annee_max")
    prix_min = request.GET.get("prix_min")
    prix_max = request.GET.get("prix_max")
    transmission = request.GET.get("transmission")

    if annee_min:
        voitures = voitures.filter(annee__gte=annee_min)
    if annee_max:
        voitures = voitures.filter(annee__lte=annee_max)
    if prix_min:
        voitures = voitures.filter(prix__gte=prix_min)
    if prix_max:
        voitures = voitures.filter(prix__lte=prix_max)
    if transmission:
        voitures = voitures.filter(transmission=transmission)

    return render(
        request,
        "voiture/user/modele_search_auth.html",
        {"modele": modele, "voitures": voitures},
    )


# ---------------------------
# DÉTAILS D'UNE VOITURE
# ---------------------------
@role_required("user")
def voiture_detail_auth(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    images_supp = Image.objects.filter(voiture=voiture)

    return render(
        request,
        "voiture/user/voiture_detail_auth.html",
        {"voiture": voiture, "images_supp": images_supp},
    )
