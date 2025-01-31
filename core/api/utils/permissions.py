from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission, ContentType
from django.db.models import QuerySet


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        permissions = request.user.role.permissions.all()
        if not permissions:
            return False

        required_permissions = getattr(view, "required_permissions", None)
        if required_permissions:
            return any(
                permissions.filter(codename=permission).exists()
                for permission in required_permissions
            )

        return True

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin' or request.user.role == 'superadmin'
    
class IsUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'user'
    


def getAllAPIPermissions(model=None) -> QuerySet[Permission]:
    """
    Retrieves permissions for models in the 'api' app.
    :param model: The model to filter permissions by (e.g. 'user')
    """
    # Filter ContentType for models in the 'api' app
    api_content_types = ContentType.objects.filter(app_label='api')

    if model: # Get all permissions related to the model
        return Permission.objects.filter(content_type__in=api_content_types, codename__contains=model)
    else: # Get all permissions related to models in the 'api' app
        return Permission.objects.filter(content_type__in=api_content_types)
