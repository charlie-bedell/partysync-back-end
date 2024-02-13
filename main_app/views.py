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
from .permissions import IsPartyHost, IsPartyGuest
...

# include the registration, login, and verification views below
# User Registration

class Home(APIView):
  def get(self,request):
    content={'message': 'Welcome to the PartySYNC api home route!'}
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

class CreatePartyView( CreateAPIView ):
   queryset = Party.objects.all()
   serializer_class = PartySerializer
   permission_classes=[permissions.IsAuthenticated]

   def perform_create(self, serializer):
     serializer.save(host=self.request.user.profile)
     
# EARLIER VERSION
# class PartyDetailView( RetrieveUpdateDestroyAPIView ):
  # permission_classes=[ permissions.IsAuthenticated, IsPartyHost ]
  # queryset = Party.objects.all()
  # serializer_class = PartySerializer

class PartyDetailView( RetrieveUpdateDestroyAPIView ):
  permission_classes=[ permissions.IsAuthenticated, IsPartyHost ]
  queryset = Party.objects.all()
  serializer_class = PartySerializer
  def get_queryset(Party):
    
    user_profile = self.request.user.profile  # Assuming each user has a related Profile
    return Invitation.objects.filter(invitee=user_profile)


class HostView ( ListAPIView ):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = PartySerializer
  queryset = Party.objects.all()
  def get_queryset(self):
    user_profile = self.request.user.profile  
    return Party.objects.filter(host=user_profile)
  
   
class InvitesView( ListAPIView ):
    permission_classes=[ permissions.IsAuthenticated]
    serializer_class = InvitationSerializer

    def get_queryset(self):
            # Filter the queryset based on the currently authenticated user
            user_profile = self.request.user.profile  # Assuming each user has a related Profile
            return Invitation.objects.filter(invitee=user_profile)


class InvitationView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPartyHost]
    serializer_class = InvitationSerializer 

    def post(self, request, *args, **kwargs):
        party_id = self.kwargs.get('party_id')
        host_profile = request.user.profile
        if Invitation.send_invitations_to_all(party_id, host_profile):
            return Response({'message': 'Invitations sent successfully'})
        else:
            return Response({'message': 'Failed to send invitations'}, status=400)
  
class InviteResponse(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsPartyGuest]
    serializer_class = InvitationSerializer
    queryset = Invitation.objects.all()

    def perform_update(self, serializer):
        status = serializer.validated_data.get('status')
        if status:
            serializer.save(status=status)
        else:
            return Response({'message': 'There was an error. Status was not provided in the request.'})
            

  #  Host can edit and delete parties
  #  Invitations