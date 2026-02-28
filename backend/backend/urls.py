from django.contrib import admin
from django.urls import path, include
from compile import urls as compile_urls
from Registration import urls as register_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("compile/", include(compile_urls)),
    path("Register/", include(register_urls)),
    path("accounts/", include("django.contrib.auth.urls")),
]
