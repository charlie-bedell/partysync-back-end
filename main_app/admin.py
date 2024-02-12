from django.contrib import admin
from .models import Party, Profile, Invitation

# Register your models here.
admin.site.register(Party)
admin.site.register(Profile)
admin.site.register(Invitation)
