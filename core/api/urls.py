from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from api.views.authViewset import LoginViewset, RegisterViewset, UserPermissionsView, ProfileViewset, ChangePasswordView, forget_password_request, forget_password_verify, delete_account, logout
from api.views.testViewset import TestViewset


urlpatterns = [
    # Auth
    path('auth/register/', RegisterViewset.as_view(), name='register'),
    path('auth/login/', LoginViewset.as_view(), name='login'),
    path('auth/forget-password/', forget_password_request, name='forget-password'),
    path('auth/forget-password/verify/', forget_password_verify, name='forget-password-verify'),

    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/permissions/', UserPermissionsView.as_view(), name='permissions'),
    path('auth/profile/', ProfileViewset.as_view(), name='profile'),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/delete-account/', delete_account, name='delete-account'),
    path('auth/logout/', logout, name='logout'),
]

router = SimpleRouter()

router.register('test', TestViewset, basename='test')

urlpatterns += router.urls