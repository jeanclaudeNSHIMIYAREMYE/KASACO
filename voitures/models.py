from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrateur'),
        ('user', 'Utilisateur'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username






class Marque(models.Model):
    
    #Représente la marque d'une voiture (Toyota, Honda, etc.)
    
    nom = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nom']
        verbose_name = "Marque"
         #verbose_name_plural = "Marques"

    def __str__(self):
        return self.nom


class Modele(models.Model):
    
    # Représente un modèle spécifique d'une marque (ex: Corolla, RAV4, Civic, etc.)
    
    marque = models.ForeignKey(Marque, on_delete=models.CASCADE, related_name='modeles')
    nom = models.CharField(max_length=100)

    class Meta:
        ordering = ['nom']
        verbose_name = "Modèle"
        verbose_name_plural = "Modèles"
        unique_together = ('marque', 'nom')

    def __str__(self):
        return f"{self.marque.nom} - {self.nom}"


class Voiture(models.Model):
    
     #Représente une voiture à vendre sur le site.
    

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
    image = models.ImageField(upload_to='voitures/', blank=True, null=True)
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='Disponible')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_ajout']
        verbose_name = "Voiture"
        verbose_name_plural = "Voitures"

    def __str__(self):
        return f"{self.marque.nom} {self.modele.nom} ({self.id})"

    def reserver(self):
        """
        Change l'état de la voiture à 'Réservée'
        """
        self.etat = 'Réservée'
        self.save()


class Reservation(models.Model):
    
    # Représente une réservation faite par un utilisateur pour une voiture.
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    voiture = models.OneToOneField(Voiture, on_delete=models.CASCADE, related_name='reservation')
    date_reservation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Réservation"
        verbose_name_plural = "Réservations"

    def __str__(self):
        return f"Réservation de {self.voiture} par {self.utilisateur.username}"


class ContactInfo(models.Model):
    
     #Contient les informations de contact affichées sur la page d'accueil.
    
    telephone_whatsapp = models.CharField(max_length=20, default='+257 69 08 02 78')
    email = models.EmailField(default='karinzi.bi.sab@gmail.com')
    adresse = models.CharField(max_length=255, default='Bujumbura - Burundi, bldg Saint Pierre Avenue de l’OUA')

    class Meta:
        verbose_name = "Information de contact"
        verbose_name_plural = "Informations de contact"

    def __str__(self):
        return "Informations de contact de KASACO"

    
    