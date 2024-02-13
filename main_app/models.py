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
          for profile in all_profiles:
              if not cls.objects.filter(party=party, invitee=profile).exists():
                cls.objects.create(party=party, invitee=profile)
      except Party.DoesNotExist:
              print(f"Party with id {party_id} does not exist.")
              return False
      except Exception as e:          
          print(f"Error sending invitations: {e}")
          return False
      return True
  
