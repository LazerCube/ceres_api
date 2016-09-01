from rest_framework import permissions

class IsSourceUserOrPost(permissions.BasePermission):
    """
    Custom permission to only allow source user to have access
    but anyone account to post
    """
    def has_object_permission(self, request, view, obj):
        if request.user == obj.source_user or request.method == "POST":
            return True
        return False

class IsSource(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.source_user:
            return True
        return False
