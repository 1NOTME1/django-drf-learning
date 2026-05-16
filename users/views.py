# region imports
from rest_framework.viewsets import ModelViewSet
from .models import UserProfile, Department
from .serializers import UserProfileSerializer, DepartmentSerializer

from .filters import (
    apply_user_filters,
    apply_department_filter,
    apply_min_age_filter,
    apply_user_ordering,
    parse_pagination_params,
    apply_max_age_filter,
    apply_department_name_filter,
    apply_is_adult_filter,
)

from .responses import (
    error_response,
    validation_error_response,
    success_response,
    list_response,
    message_response,
)

# endregion


class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    
    def get_queryset(self):
        return UserProfile.objects.select_related("department").all()

    def list(self, request):
        users = self.get_queryset()
        
        users = apply_user_filters(users, request)
        if users is None:
            return error_response("Invalid is_active value")

        users = apply_min_age_filter(users, request)
        if users is None:
            return error_response("Invalid min_age value")
        
        users = apply_max_age_filter(users, request)
        if users is None:
            return error_response("Invalid max_age value")
        
        users = apply_is_adult_filter(users, request)
        if users is None:
            return error_response("Invalid is_adult value")
        
        users = apply_department_filter(users, request)
        if users is None:
            return error_response("Invalid department value")
        
        users = apply_department_name_filter(users, request)
        if users is None:
            return error_response("Invalid department_name value")

        users = apply_user_ordering(users, request)
        if users is None:
            return error_response("Invalid ordering value")
        
        limit, offset, error_message = parse_pagination_params(request)
        
        if error_message is not None:
            return error_response(error_message, 400)
        
        users = users[offset:offset + limit]

        serializer = self.get_serializer(users, many=True)

        return list_response(serializer.data, users.count())

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        serializer.save()

        return success_response(serializer.data, status_code=201)

    def retrieve(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user)
        
        return success_response(serializer.data)

    def partial_update(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)
        
        serializer.save()
        
        return success_response(serializer.data)

    def update(self, request, pk=None):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data)
        
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)
        
        serializer.save()
        
        return success_response(serializer.data)

    def destroy(self, request, pk=None):
        user = self.get_object()
        user.delete()
        
        return message_response("User deleted")


class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all().order_by("id")
    serializer_class = DepartmentSerializer
