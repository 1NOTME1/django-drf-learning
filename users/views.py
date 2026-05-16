# region imports
from rest_framework.decorators import api_view
from rest_framework.views import APIView
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
    message_response,
    list_response,
)

from .selectors import get_user_or_none
# endregion


class UsersAPIView(APIView):
    def get(self, request):
        users = UserProfile.objects.select_related("department").all()

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

        serializer = UserProfileSerializer(users, many=True)

        return list_response(serializer.data, users.count())

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        serializer.save()

        return success_response(serializer.data, status_code=201)


class UserDetailAPIView(APIView):
    def get(self, request, user_id):
        user = get_user_or_none(user_id)

        if user is None:
            return error_response("User not found", 404)

        serializer = UserProfileSerializer(user)

        return success_response(serializer.data)

    def patch(self, request, user_id):
        user = get_user_or_none(user_id)

        if user is None:
            return error_response("User not found", 404)

        serializer = UserProfileSerializer(user, data=request.data, partial=True)

        if not serializer.is_valid():
            return validation_error_response(serializer.errors)

        serializer.save()

        return success_response(serializer.data)

    def delete(self, request, user_id):
        user = get_user_or_none(user_id)

        if user is None:
            return error_response("User not found", 404)

        user.delete()

        return message_response("User deleted")


class DepartmentsAPIView(APIView):
    def get(self, request):
        departments = Department.objects.all().order_by("id")
        serializer = DepartmentSerializer(departments, many=True)
        
        return list_response(serializer.data, departments.count())
    
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        
        if not serializer.is_valid():
            return validation_error_response(serializer.errors)
        
        serializer.save()
        
        return success_response(serializer.data, status_code=201)