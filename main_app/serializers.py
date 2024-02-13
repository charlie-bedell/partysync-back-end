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
        Profile.objects.create(user=user)

        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user',)

# class PartySerializer(serializers.ModelSerializer):
#     host = ProfileSerializer(read_only=True)
#     class Meta:
#         model = Party
#         fields = '__all__'
#         read_only_fields = ('host',)
        
class PartySerializer(serializers.ModelSerializer):
    host = ProfileSerializer(read_only=True)
    invitations = serializers.SerializerMethodField()

    class Meta:
        model = Party
        fields = '__all__'  
        read_only_fields = ('host',)

    def get_invitations(self, obj):
        if self.context.get('include_invitations', False):
            invitations = Invitation.objects.filter(party=obj)
            context = {'exclude_party': True}
            return InvitationSerializer(invitations, many=True, read_only=True, context=context).data
        return None

class InvitationSerializer(serializers.ModelSerializer):
    invitee = ProfileSerializer(read_only=True)
    # party = PartySerializer(read_only=True)

    class Meta:
        model = Invitation
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if not self.context.get('exclude_party', False):
            party_serializer=PartySerializer(instance.party, context=self.context)
            ret['party'] = party_serializer.data
        return ret