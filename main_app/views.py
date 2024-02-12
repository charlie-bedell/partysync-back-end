# from django.shortcuts import render

from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.generics import RetrieveAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveUpdateAPIView

...
from .serializers import PartySerializer, InvitationSerializer, ProfileSerializer, UserSerializer 
from .models import Party, Profile, Invitation 
...

# include the registration, login, and verification views below
# User Registration
class Home(APIView):
  def get(self,request):
    content={'message': 'Welcome to the party api home route!'}
    return Response(content)


class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': response.data
    })

# User Login
class LoginView(APIView):
  permission_classes = [permissions.AllowAny]

  def post(self, request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
      refresh = RefreshToken.for_user(user)
      return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserSerializer(user).data
      })
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# User Verification
class VerifyUserView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def get(self, request):
    user = User.objects.get(username=request.user)  # Fetch user profile
    refresh = RefreshToken.for_user(request.user)  # Generate new refresh token
    return Response({
      'refresh': str(refresh),
      'access': str(refresh.access_token),
      'user': UserSerializer(user).data
    }) 

class ProfileView(RetrieveAPIView):
  serializer_class=ProfileSerializer
  permission_classes=[permissions.IsAuthenticated]
  queryset=Profile.objects.all()

  def get_object(self):
    content={'message': 'You are viewing a profile'}
    return self.request.user.profile

# class CreatePartyView( CreateAPIView ):
#   def post():
  
# class InvitesView( ListAPIView ):
#   def get

# class PartyDetailView( RetrieveUpdateDestroyAPIView ):
#   def get():
#   def put():
#   def delete():

# class InvitationView( RetrieveUpdateAPIView ):
#   def get
#   def put