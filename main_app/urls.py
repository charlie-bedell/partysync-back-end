from django.urls import path
from .views import CreateUserView, LoginView, VerifyUsers, ProfileView

urlpatterns = [
  path('users/register/', CreateUserView.as_view(), name='register'),
  path('users/login/', LoginView.as_view(), name='login'),
  path('users/token/refresh/', VerifyUserView.as_view(), name='token_refresh'),

  path=('/profile/', ProfileView.as_view(), name='profile'),

  path=('/party/', CreatePartyView.as_view(), name='create-party'),
  path=('party/<int:id>', PartyDetailView.as_view(), name='party-detail')

  


        

]