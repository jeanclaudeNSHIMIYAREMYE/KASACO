from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # -------------------- Accueil et Auth --------------------
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('redirect/', views.redirect_by_role, name='redirect_by_role'),

    # -------------------- Dashboards --------------------
    path('dashboard/admin/', views.admin_dashboard, name='dashboard_admin'),
    path('user/home/', views.user_home, name='user_home'),

    # -------------------- Gestion utilisateurs --------------------
    path('utilisateurs/', views.utilisateurs_list, name='utilisateurs_list'),
    path('utilisateurs/supprimer/<int:user_id>/', views.supprimer_utilisateur, name='supprimer_utilisateur'),
    path('utilisateurs/changer-role/<int:user_id>/', views.changer_role, name='changer_role'),

    # -------------------- Gestion marques --------------------
    path('marques/', views.liste_marques, name='liste_marques'),
    path('marques/ajouter/', views.ajouter_marque, name='ajouter_marque'),
    path('marques/supprimer/<int:id>/', views.supprimer_marque, name='supprimer_marque'),

    # -------------------- Gestion modèles --------------------
    path('modeles/', views.liste_modeles, name='liste_modeles'),
    path('modeles/ajouter/', views.ajouter_modele, name='ajouter_modele'),
    path('modeles/supprimer/<int:id>/', views.supprimer_modele, name='supprimer_modele'),

    # -------------------- Gestion voitures --------------------
    path('voitures/', views.liste_voitures, name='liste_voitures'),
    path('voitures/ajouter/', views.ajouter_voiture, name='ajouter_voiture'),
    path('voitures/supprimer/<int:id>/', views.supprimer_voiture, name='supprimer_voiture'),
    
    #gestion du page D' acceuil de clients des voitures--------
    
   path('detail/<int:myid>/', views.detail, name='details'),
   path('checkout',views.checkout,name='checkout'),
   path('voitures/reserver/<int:voiture_id>/', views.reserver_voiture, name='reserver_voiture'),
   path('reserver/', views.reserver, name='reserver'),
    
    
]

# -------------------- Media files --------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
