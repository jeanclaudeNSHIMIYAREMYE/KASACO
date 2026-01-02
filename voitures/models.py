from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models


# =========================
# User Manager
# =========================
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser doit avoir is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser doit avoir is_superuser=True")

        return self.create_user(email, password, **extra_fields)


# =========================
# Custom User
# =========================
class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("admin", "Administrateur"),
        ("user", "Utilisateur"),
    )

    email = models.EmailField("Adresse email", unique=True)
    username = models.CharField("Nom d'utilisateur", max_length=150, unique=True)

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user",
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["username"]
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.email




# --- Marque ---
class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    logo = models.FileField(upload_to="logos", null=True, blank=True)

    class Meta:
        ordering = ["nom"]
        verbose_name = "Marque"

    def __str__(self):
        return self.nom



# --- Modele ---
class Modele(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="modeles")
    nom = models.CharField(max_length=100)
    image = models.ImageField(upload_to="modeles", null=True, blank=True)  # ImageField pour vérifier les images

    class Meta:
        ordering = ["nom"]
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        constraints = [
            models.UniqueConstraint(fields=["marque", "nom"], name="unique_marque_nom")
        ]

    def __str__(self):
        return f"{self.marque.nom} - {self.nom}"



# --- Voiture ---
class Voiture(models.Model):
    TRANSMISSION_CHOICES = [
        ("Manuelle", "Manuelle"),
        ("Automatique", "Automatique"),
        ("Autre", "Autre"),
    ]

    ETAT_CHOICES = [
        ("Disponible", "Disponible"),
        ("Réservée", "Réservée"),
        ("Vendue", "Vendue"),
    ]

    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name="voitures")
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name="voitures")
    numero_chassis = models.CharField(max_length=100, unique=True)
    numero_moteur = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    kilometrage = models.FloatField(help_text="Distance parcourue en kilomètres")
    couleur = models.CharField(max_length=50)
    cylindree_cc = models.PositiveIntegerField(verbose_name="Cylindrée (CC)")
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.FileField(upload_to="photos", null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default="Disponible")
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-date_ajout"]
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return f"{self.marque.nom} {self.modele.nom} ({self.numero_chassis})"

    def reserver(self):
        self.etat = "Réservée"
        self.save()


# --- Reservation ---
class Reservation(models.Model):
    voiture = models.OneToOneField(
        Voiture,
        on_delete=models.CASCADE,
        related_name="reservation"
    )
    utilisateur = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="reservations"
    )
    date_reservation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} → {self.voiture}"



# --- ContactInfo ---
class ContactInfo(models.Model):
    telephone_whatsapp = models.CharField(max_length=20, default="+257 69 08 02 78")
    email = models.EmailField(default="karinzi.bi.sab@gmail.com")
    adresse = models.CharField(
        max_length=255, default="Bujumbura - Burundi, bldg Saint Pierre Avenue de l’OUA"
    )

    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"

    def __str__(self):
        return "Informations de contact de KASACO"



# --- Images supplémentaires pour Voiture ---
class Image(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="voitures_supplementaires/")

    class Meta:
        verbose_name = "Image supplémentaire"
        verbose_name_plural = "Images supplémentaires"

    def __str__(self):
        return f"Image {self.id} - {self.voiture.marque.nom} {self.voiture.modele.nom}"
