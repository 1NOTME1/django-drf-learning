from rest_framework import serializers
from .models import UserProfile

class UserInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField()
    age = serializers.IntegerField()
    is_active = serializers.BooleanField()

    def validate_name(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("must be a string")
        
        name = value.strip().lower()
        if not name:
            raise serializers.ValidationError("empty")
        return name

    def validate_is_active(self, value):
        if value is not True:
            raise serializers.ValidationError("not active")
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.age = validated_data.get("age", instance.age)
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id" ,"name", "age", "is_active"]