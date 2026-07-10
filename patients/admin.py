from django.contrib import admin
from .models import ProfilPatient

@admin.register(ProfilPatient)
class ProfilPatientAdmin(admin.ModelAdmin):
    list_display  = ['user', 'telephone', 'date_naissance']
    search_fields = ['user__username']