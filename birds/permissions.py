from rest_framework import permissions
from .models import User, Project, Right

class IsProjectOwner(permissions.BasePermission):
    """
    Custom permission to only allow project owners to edit project.
    """
    def has_object_permission(self, request, view, obj):
        try:
            current_user_role = Right.objects.get(user=request.user, project=obj).role
            return current_user_role == 0
        except:
            return False


class IsRightOwner(permissions.BasePermission):
    """
    Custom permission to only allow project owners to edit rights to project.
    """
    # Restrict create object.
    def has_permission(self, request, view):
        if request.method == 'POST' and request.POST: 
            try:
                current_user_role = Right.objects.get(user=request.user, project_id=int(request.POST['project'])).role
                return current_user_role == 0
            except:
                return False
        else:
            return True

    # Restrict get, update and delete object detail. List views must be filtered.
    def has_object_permission(self, request, view, obj):
        try:
            current_user_role = Right.objects.get(user=request.user, project=obj.project).role
            return current_user_role == 0
        except:
            return False