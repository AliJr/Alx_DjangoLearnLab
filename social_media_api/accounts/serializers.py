from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'bio', 'profile_picture', 'followers')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'bio', 'profile_picture')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create a new user using the validated data
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
        )

        # Create a token for the new user
        token = Token.objects.create(user=user)

        # Return the user along with the token
        return user, token

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = get_user_model().objects.filter(username=attrs['username']).first()
        if user and user.check_password(attrs['password']):
            return user
        raise serializers.ValidationError("Invalid credentials")
