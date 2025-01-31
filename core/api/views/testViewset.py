from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from api.utils.permissions import RoleBasedPermission

class TestViewset(ViewSet):
    permission_classes = [RoleBasedPermission]
    required_permissions = ['view_company']

    def list(self, request):
        return Response({'message': 'Hello, World!'})