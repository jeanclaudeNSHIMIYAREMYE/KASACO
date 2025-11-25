from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Marque, Modele, Voiture, Reservation, ContactInfo,Commande

# --- CustomUser Admin ---
admin.site.site_header = "E_COMMERCE"
admin.site.site_title = "KASACO COMPANY"
admin.site.index_title = "VENDEUR"
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active")}
        ),
    )
    search_fields = ("username", "email")
    ordering = ("username",)

# --- Marque Admin ---
@admin.register(Marque)
class adminMarque(admin.ModelAdmin):
    list_display=["nom"]
    search_fields=['nom']

# --- Modele Admin ---
@admin.register(Modele)
class AdminModele(admin.ModelAdmin):
    list_display = ["nom", "marque"]
    list_filter = ["marque"]
    search_fields = ["nom", "marque__nom"]

# --- Voiture Admin ---
@admin.register(Voiture)
class AdminVoiture(admin.ModelAdmin):
    list_display = ["marque", "modele", "numero_chassis", "numero_moteur", "prix", "etat","photo" ,"date_ajout"]
    list_filter = ["marque", "modele", "etat", "transmission"]
    list_editable=["prix"]
    search_fields = ["numero_chassis", "numero_moteur", "marque__nom", "modele__nom"]

# --- Reservation Admin ---
@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ["voiture", "utilisateur", "date_reservation"]
    search_fields = ["voiture__numero_chassis", "utilisateur__username"]
    list_filter = ["date_reservation"]

# --- Contact Info Admin ---
@admin.register(ContactInfo)
class AdminContactInfo(admin.ModelAdmin):
    list_display = ["telephone_whatsapp", "email", "adresse"]
    
@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
    list_display=['nom','pays','items','total']