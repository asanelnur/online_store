from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from users import services, serializers


# Create your views here.


class UserViewSet(ViewSet):
    user_service: services.UserServicesInterface = services.UserServicesV1()

    def create_user(self, request, *args, **kwargs):
        serializer = serializers.CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.user_service.create_user(data=serializer.validated_data)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user(self, request, *args, **kwargs):
        serializer = serializers.GetUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tokens = self.user_service.get_user(data=serializer.validated_data)

        return Response(tokens)
