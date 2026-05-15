# region imports
from rest_framework.decorators import api_view

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


@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.select_related("department").all()

    users = apply_user_filters(users, request)
    if users is None:
        return error_response("Invalid is_active value")

    users = apply_min_age_filter(users, request)
    if users is None:
        return error_response("Invalid min_age value")
    
    users = apply_department_filter(users, request)
    if users is None:
        return error_response("Invalid department value")

    users = apply_user_ordering(users, request)
    if users is None:
        return error_response("Invalid ordering value")
    
    users = apply_max_age_filter(users, request)
    if users is None:
        return error_response("Invalid max_age value")
    
    users = apply_department_name_filter(users, request)
    if users is None:
        return error_response("Invalid department_name value")
    
    users = apply_is_adult_filter(users, request)
    if users is None:
        return error_response("Invalid is_adult value")
    
    limit, offset, error_message = parse_pagination_params(request)
    
    if error_message is not None:
        return error_response(error_message, 400)
    
    users = users[offset:offset + limit]
        

    serializer = UserProfileSerializer(users, many=True)

    return list_response(serializer.data, users.count())


@api_view(["GET"])
def get_user_view(request, user_id):
    user = get_user_or_none(user_id)

    if user is None:
        return error_response("User not found", 404)

    serializer = UserProfileSerializer(user)

    return success_response(serializer.data)


@api_view(["POST"])
def create_user_view(request):
    serializer = UserProfileSerializer(data=request.data)

    if not serializer.is_valid():
        return validation_error_response(serializer.errors)

    serializer.save()

    return success_response(serializer.data, status_code=201)


@api_view(["PATCH"])
def update_user_view(request, user_id):
    user = get_user_or_none(user_id)

    if user is None:
        return error_response("User not found", 404)

    serializer = UserProfileSerializer(user, data=request.data, partial=True)

    if not serializer.is_valid():
        return validation_error_response(serializer.errors)

    serializer.save()

    return success_response(serializer.data)


@api_view(["DELETE"])
def delete_user_view(request, user_id):
    user = get_user_or_none(user_id)

    if user is None:
        return error_response("User not found", 404)

    user.delete()

    return message_response("User deleted")


@api_view(["GET"])
def departments_list_view(request):
    departments = Department.objects.all().order_by("id")
    
    serializer = DepartmentSerializer(departments, many=True)
    
    return list_response(serializer.data, departments.count())


@api_view(["POST"])
def create_department_view(request):
    
    serializer = DepartmentSerializer(data=request.data)
    
    if not serializer.is_valid():
        return validation_error_response(serializer.errors)
    
    serializer.save()
    
    return success_response(serializer.data, status_code=201)

