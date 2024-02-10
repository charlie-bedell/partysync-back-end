from django.db import models



class Profile(models.Model):
  user_id = models.OneToOneField(User),
  
  # stretch goal - add image here
  def __str__(self):
    return self.username

class Party(models.Model):
  name = models.CharField(max_length=100, required=True),
  location = models.CharField(max_length=100, requiered=True),
  start_time = models.DateTimeField(required=True),
  end_time = models.DateTimeField(),
  description = models.TextField()
  host_id = models.ForeignKey(Profile, on_delete=models.CASCADE, default='1')

  def __str__(self):
    return self.name
  
class Invitation(models.Model):
  party = models.FoerignKey(Party, on_delete=models.CASCADE, default='1')

