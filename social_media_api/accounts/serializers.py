from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "email", "bio", "profile_picture", "followers")


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("username", "password")

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
