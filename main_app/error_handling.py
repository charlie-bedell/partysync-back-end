
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status

class ProfileNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested profile was not found.'
    default_code = 'profile_not_found'

class PartyNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested party was not found.'
    default_code = 'party_not_found'

class InvitationNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'The requested invitation was not found.'
    default_code = 'invitation_not_found'