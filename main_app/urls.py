from django.urls import path
from .views import Home, CreateUserView, LoginView, VerifyUserView, ProfileView, CreatePartyView, PartyDetailView, InvitationView, InvitesView
# InvitesView, InvitationView

urlpatterns = [
  path('', Home.as_view(), name='home'),

  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),
  path('profile/', ProfileView.as_view(), name='profile'),
  path('party/', CreatePartyView.as_view(), name='create-party'),
  path('party/<int:pk>/', PartyDetailView.as_view(), name='party-detail'),
  path('profile/invites/', InvitesView.as_view(), name='invites' ),
  path('profile/invite/<int:party_id>/', InvitationView.as_view(), name='invitation-view/' )  
]