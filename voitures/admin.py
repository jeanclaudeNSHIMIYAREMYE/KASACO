from django.contrib import admin
from .models import CustomUser,Marque,Modele,Voiture, Reservation,ContactInfo

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Marque)
admin.site.register(Modele)
admin.site.register(Voiture)
admin.site.register(Reservation)
admin.site.register(ContactInfo)