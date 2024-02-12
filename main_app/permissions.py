from rest_framework import permissions
from .models import Party, Invitation

class IsPartyHost(permissions.BasePermission):
  
   def has_object_permission(self, request, view, obj):
        # obj here is a Party instance
        if not request.user or not request.user.is_authenticated:
            return False
        return obj.host == request.user.profile
   

class IsPartyGuest(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        return obj.invitee == request.user.profile

