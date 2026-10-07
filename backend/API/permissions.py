from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import AnonymousUser


class IsAdminOrReadOnly(BasePermission):
    """
    Permet aux utilisateurs d'effectuer des requêtes 'GET', 'HEAD', 'OPTIONS'
    Nécessaire d'être administrateur dans le cas contraîre
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or type(request.user) != AnonymousUser
            and request.user.is_admin
        )


class IsUserOrAdmin(BasePermission):
    """
    Nécessite d'être l'utilisateur en question ou l'administrateur
    """

    def has_permission(self, request, view):
        # Vérifie que l'utilisateur est au niveau du router ou pas
        if type(view).__name__ == "UtilisateurViewSet":
            field = view.lookup_field
        else:
            field = view.router_lookup_field
        return bool(
            type(request.user) != AnonymousUser
            and (request.user.is_admin or request.user.uuid == view.kwargs.get(field))
        )
