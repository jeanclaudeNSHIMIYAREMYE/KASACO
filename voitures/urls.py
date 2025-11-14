# fichier : urls.py
from django.urls import path
from . import views  # Assure-toi d'importer views depuis ton app

urlpatterns = [
    path('', views.home, name='home'),  # Page d'accueil
    
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("redirect/", views.redirect_by_role, name="redirect_by_role"),

    path('dashboard/admin/', views.admin_dashboard, name='dashboard_admin'),
    path("user/home/", views.user_home, name="user_home"),
]
