from django import views
from django.urls import path
from .views import AdminRegister, RegisterView, AdminRegister
from rest_framework_simplejwt import views as jwt_views
urlpatterns = [
    path("User/", RegisterView.as_view(), name="register"),
    path("AdminUser/", AdminRegister.as_view(), name="admin_register"),
    path("login/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]