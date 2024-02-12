from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Party, Profile, Invitation

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Add a password field, make it write-only

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  # Ensures the password is hashed correctly
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)

class PartySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(many= True, read_only=True)
    class Meta:
        model = Party
        fields = '__all__'

class InvitationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    party = PartySerializer(read_only=True)
    class Meta:
        model = Invitation
        fields = '__all__'
