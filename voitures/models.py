from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.exceptions import ValidationError

# --- Custom User ---
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('user', 'Utilisateur'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    class Meta:
        ordering = ['username']

    def __str__(self):
        return self.username


# --- Marque ---
class Marque(models.Model):
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Marque"

    def __str__(self):
        return self.nom


# --- Modele ---
class Modele(models.Model):
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='modeles')
    nom = models.CharField(max_length=100)

    class Meta:
        ordering = ['nom']
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        unique_together = ('marque', 'nom')

    def __str__(self):
        return f"{self.marque.nom} - {self.nom}"


# --- Voiture ---
class Voiture(models.Model):
    TRANSMISSION_CHOICES = [
        ('Manuelle', 'Manuelle'),
        ('Automatique', 'Automatique'),
        ('Autre', 'Autre'),
    ]

    ETAT_CHOICES = [
        ('Disponible', 'Disponible'),
        ('Réservée', 'Réservée'),
        ('Vendue', 'Vendue'),
    ]

    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='voitures')
    modele = models.ForeignKey(Modele, on_delete=models.CASCADE, related_name='voitures')
    numero_chassis = models.CharField(max_length=100, unique=True)
    numero_moteur = models.CharField(max_length=100)
    annee = models.PositiveIntegerField()
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    kilometrage = models.FloatField(help_text="Distance parcourue en kilomètres")
    couleur = models.CharField(max_length=50)
    cylindree_cc = models.PositiveIntegerField(verbose_name="Cylindrée (CC)")
    prix = models.DecimalField(max_digits=12, decimal_places=2)
    photo = models.FileField(upload_to='photos', null=True, blank=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='Disponible')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return f"{self.marque.nom} {self.modele.nom} ({self.numero_chassis})"

    def reserver(self):
        self.etat = 'Réservée'
        self.save()


# --- Reservation ---

class Reservation(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    voiture = models.ForeignKey(
        Voiture,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_debut = models.DateTimeField(null=True, blank=True)  # optionnel : pour réservation à partir d'une date précise
    date_fin = models.DateTimeField(null=True, blank=True)    # optionnel : pour réservation avec fin

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"
        ordering = ['-date_reservation']

    def __str__(self):
        return f"Réservation de {self.voiture} par {self.utilisateur.username}"

    def clean(self):
        """
        Validation pour empêcher qu'une voiture soit réservée plusieurs fois 
        pour la même période (si date_debut et date_fin sont définis)
        """
        if self.date_debut and self.date_fin:
            # Vérifie qu'aucune réservation existante ne chevauche les dates
            conflit = Reservation.objects.filter(
                voiture=self.voiture,
                date_fin__gte=self.date_debut,
                date_debut__lte=self.date_fin
            ).exclude(pk=self.pk)
            if conflit.exists():
             raise ValidationError("Cette voiture est déjà réservée pour cette période.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Appelle clean() pour valider avant sauvegarde
        super().save(*args, **kwargs)


# --- ContactInfo ---
class ContactInfo(models.Model):
    telephone_whatsapp = models.CharField(max_length=20, default='+257 69 08 02 78')
    email = models.EmailField(default='karinzi.bi.sab@gmail.com')
    adresse = models.CharField(max_length=255, default='Bujumbura - Burundi, bldg Saint Pierre Avenue de l’OUA')

    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"

    def __str__(self):
        return "Informations de contact de KASACO"
    
class Commande(models.Model):
        items=models.CharField( max_length=150)
        total=models.CharField(max_length=300)
        nom=models.CharField(max_length=340)
        email=models.EmailField()
        address=models.CharField(max_length=300)
        ville=models.CharField(max_length=200)
        pays=models.CharField(max_length=100)
        zipcode=models.CharField(max_length=200)
        date_commande=models.DateTimeField(auto_now=True)
        
        class meta:
            ordering=["-date_commande"]
        
        