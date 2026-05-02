# region imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

from .filters import (
    apply_user_filters,
    apply_department_filter,
    apply_min_age_filter,
    apply_user_ordering,
)

from .responses import (
    error_response,
    validation_error_response,
    success_response,
    message_response,
)

# endregion

def get_user_or_none(user_id):
    try:
        return UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return None


@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.all()

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

    serializer = UserProfileSerializer(users, many=True)

    return Response(
        {"status": "ok", "data": serializer.data, "count": users.count()},
        status=200,
    )


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
