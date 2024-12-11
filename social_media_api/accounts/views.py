from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, RegistrationSerializer

from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate




# Read only view for User Serializer
class UserView(APIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    
    def get(self, request):
        # Only authenticated users can access this view
        serializers = UserSerializer(request.user)
        return Response(serializers.data)

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    #serializer_class = UserSerializer
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)