from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from api.models import User, Role, UserRole
from api.utils.permissions import getAllAPIPermissions

class Command(BaseCommand):
    help = 'Create a superuser with predefined credentials'

    def handle(self, *args, **kwargs):
        # Define superuser details
        username = 'admin'
        email = 'admin@gmail.com'
        password = 'password'
        # Check if superuser already exists
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)  # Ensure password is hashed
            user.is_superuser = True
            user.is_staff = True
            user.save()

            # Get or create the SuperAdmin role
            role, created = Role.objects.get_or_create(name='SuperAdmin')

            # Get all permissions and assign them to the role
            permissions = getAllAPIPermissions()
            role.permissions.set(permissions)

            # Get or create the user-role association
            UserRole.objects.get_or_create(user=user, role=role)

            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" already exists.'))
