from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    website = models.URLField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    user = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return self.name