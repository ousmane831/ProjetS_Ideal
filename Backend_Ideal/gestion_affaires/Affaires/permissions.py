# permissions.py
from rest_framework import permissions

class IsApporteur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'apporteuraffaires')

class IsChercheur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'chercheuraffaires')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Tout utilisateur connecté peut lire (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated

        # Seuls les administrateurs peuvent modifier
        return request.user.is_authenticated and hasattr(request.user, 'administrateur')
class IsAdministrateur(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'administrateur')

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and hasattr(request.user, 'administrateur')


