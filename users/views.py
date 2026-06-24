from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (MyTokenSerializer, RegisterMedecinSerializer,
                           RegisterPatientSerializer, RegisterResponsableSerializer)

class MyLoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class   = MyTokenSerializer

class RegisterMedecinView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterMedecinSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Médecin créé"}, status=201)
        return Response(serializer.errors, status=400)

class RegisterPatientView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterPatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Patient créé"}, status=201)
        return Response(serializer.errors, status=400)

class RegisterResponsableView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterResponsableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Responsable créé"}, status=201)
        return Response(serializer.errors, status=400)