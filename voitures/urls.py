from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    # -------------------- Accueil et Auth --------------------
    path("", views.home, name="home"),
    path("inscrire/", views.signup_view, name="signup"),
    path("connexion/", views.login_view, name="login"),
    path("verification", views.verification_email, name="verification"),
    path("changement/<str:email>/", views.changementCode, name="changementCode"),
    path("deconnexion/", views.logout_view, name="logout"),
    path("redirect/", views.redirect_by_role, name="redirect_by_role"),
    path("pourquoi-kasaco/", views.pourquoi_kasaco, name="pourquoi_kasaco"),
    # -------------------- Dashboards --------------------
    path("tableau_de_bord/admin/", views.admin_dashboard, name="dashboard_admin"),
    path("utilisateur/acceuil/", views.user_home, name="user_home"),
    # -------------------- Gestion utilisateurs --------------------
    path("utilisateurs/", views.utilisateurs_list, name="utilisateurs_list"),
    path(
        "utilisateurs/supprimer/<int:user_id>/",
        views.supprimer_utilisateur,
        name="supprimer_utilisateur",
    ),
    path(
        "utilisateurs/changer-role/<int:user_id>/",
        views.changer_role,
        name="changer_role",
    ),
    # -------------------- Gestion marques --------------------
    path("marques/", views.liste_marques, name="liste_marques"),
    path("marques/ajouter/", views.add_mark, name="add_mark"),
    path(
        "marques/supprimer/<int:id>/", views.supprimer_marque, name="supprimer_marque"
    ),
    # -------------------- Gestion modèles --------------------
    path("modeles/", views.liste_modeles, name="liste_modeles"),
    path("modeles/ajouter/", views.ajouter_modele, name="ajouter_modele"),
    path(
        "modeles/supprimer/<int:id>/", views.supprimer_modele, name="supprimer_modele"
    ),
    # -------------------- Gestion voitures --------------------
    path("voitures/", views.liste_voitures, name="liste_voitures"),
    path("voitures/ajouter/", views.ajouter_voiture, name="ajouter_voiture"),
    path(
        "voitures/supprimer/<int:id>/",
        views.supprimer_voiture,
        name="supprimer_voiture",
    ),
    # -------------------- Pages utilisateurs --------------------
    path("detail/<int:myid>/", views.detail, name="details"),
    path(
        "voitures/reserver/<int:voiture_id>/",
        views.reserver_voiture,
        name="reserver_voiture",
    ),
    path("info/", views.info, name="info"),
    path("contact/", views.contact_view, name="contact"),
    path("mes-reservations/", views.mes_reservations, name="mes_reservations"),
    path(
        "reserver/voitures/",
        views.disponible_liste_voitures,
        name="reserver_liste_voitures",
    ),
    path(
        "voiture/<int:voiture_id>/reserver/",
        views.reserver_voiture,
        name="reserver_voiture",
    ),
    path(
        "reservation/annuler/<int:reservation_id>/",
        views.annuler_reservation,
        name="annuler_reservation",
    ),
    #################################
    path("list", views.marque_list, name="marque_list"),
    path("marque/<int:marque_id>/", views.modele_list, name="modele_list"),
    path("modele/<int:modele_id>/", views.modele_search, name="modele_search"),
    path("voiture/<int:voiture_id>/", views.voiture_detail, name="voiture_detail"),
]

# -------------------- Media files --------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
