from rest_framework import permissions
from .models import User, Project, Right

class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow project owners to edit.
    Users without rights or unauthenticated users can only view project list.
    """

    def has_object_permission(self, request, view, obj):
        user_rights_list = Right.objects.filter(user=request.user, project=obj)
        if len(user_rights_list) == 0:
            return False

        user_role = user_rights_list[0].get_role_display()
        return user_role == "owner"


class CanCRUDUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    # Is applied on object detail only. List views must be filtered.
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.user.is_manager and not obj.is_staff:
            return True
        elif obj.username == request.user.username:
            return True
        else:
            return False

class CanCRUDMeal(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    # Is applied on object detail only. List views must be filtered.
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.user.is_manager and not obj.user.is_staff:
            return True
        elif request.user.username == obj.user.username:
            return True
        else:
            return False