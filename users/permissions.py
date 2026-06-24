from rest_framework.permissions import BasePermission

class IsResponsable(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "responsable"

class IsMedecin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "medecin"

class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "patient"

class IsMedecinOrResponsable(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["medecin", "responsable"]

class IsAnyRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["responsable", "medecin", "patient"]