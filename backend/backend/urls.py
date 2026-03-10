from django.contrib import admin
from django.urls import path, include
from rest_framework import settings
from compile import urls as compile_urls
from Registration import urls as register_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin_permissions/", admin.site.urls),
    path("Processing/", include(compile_urls)),
    path("Register/", include(register_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
