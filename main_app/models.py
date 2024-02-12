from django.db import models
from django.contrib.auth.models import User

INVITE_STATUS = [
  ('Pending', 'Pending'),
  ('Maybe', 'Maybe'),
  ('Yes', 'Yes'),
  ('No', 'No')  
]

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
  # stretch goal - add image here
  def __str__(self):
    return self.user.username

class Party(models.Model):
  party_name = models.CharField(max_length=100)
  location = models.CharField(max_length=100)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField(blank=True, null=True)
  description = models.TextField()
  host = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='party')

  def __str__(self):
    return self.name
  
class Invitation(models.Model):
  party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='invitation')
  invitee = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name='invitation')
  status = models.CharField(max_length=7, choices=INVITE_STATUS, default=INVITE_STATUS[0][0])

  @classmethod
  def send_invitations_to_all(cls, party_id, host_profile):
      try:
          party = Party.objects.get(id=party_id, host_id=host_profile.id)
          all_profiles = Profile.objects.exclude(id=host_profile.id)
          invitations = [Invitation(party=party, invitee=profile) for profile in all_profiles]
          Invitation.objects.bulk_create(invitations)
      except Exception as e:
          # Log the exception or handle it accordingly
          print(f"Error sending invitations: {e}")
          return False  # Indicate failure
  
  # @classmethod
  # def respond_to_invite(cls, party_id, invitee_profile):
  #   try:

  #   except Exception as e:
  #       print(f"Error responding to invitation: {e}")
  #       return False 