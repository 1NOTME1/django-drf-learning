# region imports
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import UserProfile
from .serializers import UserProfileSerializer

# endregion

# region helpers


def error_response(message, status_code=400):
    return Response({"status": "error", "message": message}, status=status_code)


def validation_error_response(errors, status_code=400):
    return Response({"status": "error", "errors": errors}, status=status_code)


def success_response(data=None, status_code=200):
    return Response({"status": "ok", "data": data}, status=status_code)


def message_response(message, status_code=200):
    return Response({"status": "ok", "message": message}, status=status_code)


def get_user_or_none(user_id):
    try:
        return UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return None


def apply_user_filters(users, request):
    name = request.query_params.get("name")
    is_active_param = request.query_params.get("is_active")
    active_values = {"true": True, "false": False}

    if is_active_param is not None and is_active_param not in active_values:
        return None
    if is_active_param is not None:
        users = users.filter(is_active=active_values[is_active_param])

    if name is not None:
        name = name.strip()
        if name:
            users = users.filter(name__icontains=name)
    return users


def apply_user_ordering(users, request):
    allowed_ordering = ["age", "-age", "name", "-name"]
    ordering = request.query_params.get("ordering")

    if ordering is not None and ordering not in allowed_ordering:
        return None
    if ordering is not None:
        users = users.order_by(ordering)

    return users


def apply_min_age_filter(users, request):
    min_age = request.query_params.get("min_age")

    if min_age is None:
        return users

    try:
        min_age = int(min_age)
    except (ValueError, TypeError):
        return None

    if min_age < 0:
        return None

    users = users.filter(age__gte=min_age)

    return users


# endregion


@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.all()

    users = apply_user_filters(users, request)
    if users is None:
        return error_response("Invalid is_active value")

    users = apply_min_age_filter(users, request)
    if users is None:
        return error_response("Invalid min_age value")

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
