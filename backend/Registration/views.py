from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUserModel
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser

class RegisterView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]

    def post(self, request):
        email = request.data.get("email")
        phoneNumber= request.data.get("phone")
        password = request.data.get("password")

        if not email or not password or not phoneNumber:
            return Response({"detail": "Email, password, and phone are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUserModel.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUserModel.objects.create_user(email=email, password=password, phone=phoneNumber)
        user.save()

        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)


        
class AdminRegister(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    def post(self, request):
        email = request.data.get("email")
        phoneNumber= request.data.get("phone")
        password = request.data.get("password")

        if not email or not password or not phoneNumber:
            return Response({"detail": "Email, password, and phone are required."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUserModel.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUserModel.objects.create_superuser(email=email, password=password, phone=phoneNumber)
        user.save()

        return Response({"detail": "Admin User registered successfully."}, status=status.HTTP_201_CREATED)
