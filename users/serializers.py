from rest_framework import serializers

from users import models


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'password')



class GetUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
