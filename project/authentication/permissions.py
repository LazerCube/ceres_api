from rest_framework import permissions
from oauth2_provider.ext.rest_framework import TokenHasScope, TokenHasReadWriteScope

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj == request.user

class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False

class IsAuthenticatedOrTokenHasScope(permissions.BasePermission):
    """
    The user is authenticated using some backend or the token has the right scope
    This is usefull when combined with the DjangoModelPermissions to allow people browse the browsable api's
    if they log in using the a non token bassed middleware,
    and let them access the api's using a rest client with a token
    """
    def has_permission(self, request, view):
        is_authenticated = permissions.IsAuthenticated()
        token_has_scope = TokenHasScope()
        return is_authenticated.has_permission(request, view) or token_has_scope.has_permission(request, view)

class IsAuthenticatedOrTokenHasReadWriteScope(permissions.BasePermission):
    def has_permission(self, request, view):
        is_authenticated = permissions.IsAuthenticated()
        token_has_read_write_scope = TokenHasReadWriteScope()
        return is_authenticated.has_permission(request, view) or token_has_read_write_scope.has_permission(request, view)
