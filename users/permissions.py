from rest_framework.permissions import BasePermission
from .models import User


class IsResponsable(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.RESPONSABLE
        )


class IsMedecin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.MEDECIN
        )


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == User.Role.PATIENT
        )


class IsMedecinOrResponsable(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [
                User.Role.MEDECIN,
                User.Role.RESPONSABLE
            ]
        )


class IsAnyRole(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in [
                User.Role.RESPONSABLE,
                User.Role.MEDECIN,
                User.Role.PATIENT
            ]
        )