from django.contrib import admin
from .models import ProfilMedecin

@admin.register(ProfilMedecin)
class ProfilMedecinAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialite', 'telephone']