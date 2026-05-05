from rest_framework import serializers
from .models import UserProfile, Department


class UserProfileSerializer(serializers.ModelSerializer):

    department_name = serializers.CharField(source="department.name", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "name", "age", "is_active", "department", "department_name"]

    def validate(self, attrs):
        is_active = attrs.get("is_active", self.instance.is_active if self.instance else None)
        department = attrs.get("department", self.instance.department if self.instance else None)

        if is_active is False and department is None:
            raise serializers.ValidationError("Inactive user must have department")

        return attrs
    
    def validate_name(self, value):
        name = value.strip()
        if not name:
            raise serializers.ValidationError("Name cannot be empty")
        return name

    def validate_age(self, value):
        if value < 0 or value > 120:
            raise serializers.ValidationError("Age must be between 0 and 120")
        return value
    
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]
    
    def validate_name(self, value):
        name = value.strip()

        if not name:
            raise serializers.ValidationError("Name cannot be empty")

        if len(name) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long")

        return name
