from django.contrib import admin
from .models import CustomUser, Marque, Modele, Voiture, Reservation, ContactInfo

# --- CustomUser Admin ---
admin.site.register(CustomUser)

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
    list_display = ["marque", "modele", "numero_chassis", "numero_moteur", "prix", "etat","image" ,"date_ajout"]
    list_filter = ["marque", "modele", "etat", "transmission"]
    search_fields = ["numero_chassis", "numero_moteur", "marque__nom", "modele__nom"]

# --- Reservation Admin ---
@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ["voiture", "utilisateur", "date_reservation"]
    search_fields = ["voiture__numero_chassis", "utilisateur__username"]

# --- Contact Info Admin ---
@admin.register(ContactInfo)
class AdminContactInfo(admin.ModelAdmin):
    list_display = ["telephone_whatsapp", "email", "adresse"]
