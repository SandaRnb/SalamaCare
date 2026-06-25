from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    MyTokenSerializer,
    RegisterMedecinSerializer,
    RegisterPatientSerializer,
    RegisterResponsableSerializer,
    ChangePasswordSerializer,
)


# ─── Login
class MyLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class   = MyTokenSerializer


# ─── Inscription Médecin
class RegisterMedecinView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterMedecinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Médecin créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Inscription Patient
class RegisterPatientView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Patient créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Inscription Responsable
class RegisterResponsableView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Responsable créé avec succès"},
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# ─── Changement mot de passe
class ChangePasswordView(APIView):

    def put(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Mot de passe modifié avec succès"}
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )