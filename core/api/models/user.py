from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
import uuid

class UserManager(BaseUserManager):
    """
    Custom manager for the User model where email is the unique identifier
    for authentication instead of usernames.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True, related_name='permissions')

    def __str__(self):
        return self.name

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png', null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    remember_token = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)

    # Attach the custom user manager
    objects = UserManager()

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    company = models.ForeignKey("api.company", on_delete=models.CASCADE, null=True, blank=True)

    @property
    def permissions(self):
        return self.role.permissions.all()

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

# Automatically delete image files when User is deleted
@receiver(post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(False)
