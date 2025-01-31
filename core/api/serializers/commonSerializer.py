from api.models import User
from rest_framework import serializers
import re

class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    def validate_username(self, username):
        norm_username = username.lower()
        try:
            User.objects.get(username=norm_username)
            raise serializers.ValidationError("This username already exists.")
        except User.DoesNotExist:
            pass
        pattern = r"^[a-zA-Z][a-zA-Z0-9_.]*$"
        if not re.match(pattern, username):
            raise serializers.ValidationError(
                'Invalid username. It should start with a letter and can contain letters, numbers, underscores, and dots.'
            )
        return norm_username
    def validate_email(self, value):
        if not value:
            return None
        norm_email = value.lower()
        try:
            User.objects.get(email=norm_email)
            raise serializers.ValidationError("This email already exists.")
        except User.DoesNotExist:
            pass
        return norm_email