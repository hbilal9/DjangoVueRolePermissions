from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_active', 'is_staff', 'is_superuser', 'date_joined')
    list_display_links = ('id', 'username')
    list_filter = ('role', 'is_active', 'date_joined')
    search_fields = ('username', 'email')
    list_per_page = 25
    
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25

class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role', 'company')
    list_display_links = ('id', 'user')
    search_fields = ('user', 'role','company')
    list_per_page = 25

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'address', 'phone', 'email', 'website', 'is_active')
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'name')
    search_fields = ('name', 'address', 'phone', 'email', 'website')
    list_per_page = 25

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'codename')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'content_type', 'codename')
    list_per_page = 25


admin.site.register(User, UserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Permission, PermissionAdmin)
