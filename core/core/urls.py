from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from api.views.webhookViewset import github_webhook

admin.site.site_header = "CipherHaven Admin"
admin.site.site_title = "CipherHaven Admin Dashboard"
admin.site.index_title = "Welcome to CipherHaven Administartion Dashboard"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('webhook/github/', github_webhook, name='github_webhook'),
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
