from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import (
    Commande, ContactInfo, CustomUser, Marque, Modele, Image,
    Reservation, Voiture
)

# ----------------- Admin Site Header -----------------
admin.site.site_header = "E_COMMERCE"
admin.site.site_title = "KASACO COMPANY"
admin.site.index_title = "VENDEUR"


# ----------------- CustomUser Admin -----------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active")
    ordering = ("username",)
    search_fields = ("username", "email")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "email")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )


# ----------------- Marque Admin -----------------
@admin.register(Marque)
class AdminMarque(admin.ModelAdmin):
    list_display = ["nom"]
    search_fields = ["nom"]
    ordering = ["nom"]


# ----------------- Modele Admin -----------------
@admin.register(Modele)
class AdminModele(admin.ModelAdmin):
    list_display = ["nom", "marque"]
    list_filter = ["marque"]
    search_fields = ["nom", "marque__nom"]
    ordering = ["marque__nom", "nom"]


# ----------------- Image Inline pour Voiture -----------------
class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ('image', 'image_tag',)
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Aperçu'


# ----------------- Voiture Admin -----------------
@admin.register(Voiture)
class AdminVoiture(admin.ModelAdmin):
    list_display = [
        "marque",
        "modele",
        "numero_chassis",
        "numero_moteur",
        "prix",
        "etat",
        "photo_tag",
        "date_ajout",
    ]
    list_filter = ["marque", "modele", "etat", "transmission"]
    list_editable = ["prix"]
    search_fields = ["numero_chassis", "numero_moteur", "marque__nom", "modele__nom"]
    ordering = ["-date_ajout"]
    inlines = [ImageInline]

    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.photo.url)
        return "-"
    photo_tag.short_description = 'Photo'


# ----------------- Reservation Admin -----------------
@admin.register(Reservation)
class AdminReservation(admin.ModelAdmin):
    list_display = ["voiture", "utilisateur", "date_reservation"]
    list_filter = ["date_reservation"]
    search_fields = ["voiture__numero_chassis", "utilisateur__username"]
    ordering = ["-date_reservation"]


# ----------------- Contact Info Admin -----------------
@admin.register(ContactInfo)
class AdminContactInfo(admin.ModelAdmin):
    list_display = ["telephone_whatsapp", "email", "adresse"]


# ----------------- Commande Admin -----------------
@admin.register(Commande)
class AdminCommande(admin.ModelAdmin):
    list_display = ["nom", "pays", "items", "total", "date_commande"]
    ordering = ["-date_commande"]
    search_fields = ["nom", "email", "ville", "pays"]


# ----------------- Image Admin -----------------
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('voiture', 'image_tag')
    search_fields = ["voiture__numero_chassis"]

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height:auto;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Aperçu'
