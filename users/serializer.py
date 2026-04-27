from rest_framework import serializers
from .models import UserProfile

class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "age"]
        
