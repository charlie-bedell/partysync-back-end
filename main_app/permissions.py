from rest_framework import permissions
from .models import Party, Invitation

class IsPartyHost(permissions.BasePermission):
  

   def has_object_permission(self, request, view, obj):
        # obj here is a Party instance
        # Check if the user is authenticated and is the host of the party
        return obj.host == request.user.profile.id
