from rest_framework import serializers
from api.models import User
import re

from rest_framework import serializers
from api.models import User
import re

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("This username already exists.")

        pattern = r"^[a-zA-Z][a-zA-Z0-9_.]*$"
        if not re.match(pattern, username):
            raise serializers.ValidationError(
                'Invalid username. It should start with a letter and can contain letters, numbers, underscores, and dots.'
            )
        if len(username) < 4:
            raise serializers.ValidationError("Username must be at least 4 characters long.")
        return username

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        
        # only allow email with domain @gmail.com or @yahoo.com or @hotmail.com
        pattern = r"^[a-zA-Z0-9_.+-]+@(gmail|yahoo|hotmail)\.com$"
        if not re.match(pattern, value):
            raise serializers.ValidationError("This email is not allowed.")
        return value
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password != self.initial_data.get('confirm_password'):
            raise serializers.ValidationError("Confirm password must match.")
        return password
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data['password']
        username = validated_data['username'].lower()
        email = validated_data['email'].lower()

        validated_data['username'] = username
        validated_data['email'] = email

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        return user

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.DateTimeField(read_only=True)
    user_permissions = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    is_email_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    # notifications = NotificationSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'is_active', 'date_joined', 'phone', 'is_email_verified',
            'last_login', 'avatar', 'remarks', 'user_permissions'
        ]

    def get_user_permissions(self, obj):
        permissions = set()
        permissions.update(obj.role.permissions.all().values_list("codename", flat=True))
        return permissions

    def get_role(self, obj):
        return obj.role.role.name if obj.role else 'user'

class ForgotPasswordVerifySerializer(serializers.Serializer):
    # email = serializers.EmailField()
    id = serializers.IntegerField()
    token = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields.pop('confirm_password')

    def validate(self, data):
        if len(data.get('password')) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long."})
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Confirm password must match."})
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields.pop('confirm_password')

    def validate(self, data):
        if len(data.get('new_password')) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long."})
        if data.get('new_password') != data.get('confirm_password'):
            raise serializers.ValidationError({"confirm_password": "Confirm password must match."})

        user = self.context['request'].user
        if not user.check_password(data.get('current_password')):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})
        return data
    
