from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializer import UserInputSerializer, UserProfileSerializer

@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.all()
    
    min_age = request.query_params.get("min_age")
    is_active_param = request.query_params.get("is_active")
    ordering = request.query_params.get("ordering")
    
    try:
        min_age = int(min_age)
    except (TypeError, ValueError):
        min_age = None
        
    if min_age is not None:
        users = users.filter(age__gte=min_age)
    
    if is_active_param == "true":
        users = users.filter(is_active=True)
    elif is_active_param == "false":
        users = users.filter(is_active=False)
    
    if ordering == "age":
        users = users.order_by("age")
    elif ordering == "-age":
        users = users.order_by("-age")
    
    serializer = UserProfileSerializer(users, many=True)

    return Response({
        "status": "ok",
        "data": serializer.data,
        "count": users.count()
    })

@api_view(["GET"])
def get_user_view(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response({
            "status": "error",
            "message": "User not found"
        }, status=404)
        
    serializer = UserProfileSerializer(user)
    
    return Response({
        "status": "ok",
        "data": serializer.data
    }, status=200)
        
        
@api_view(['POST'])
def create_user_view(request):
    serializer = UserProfileSerializer(data = request.data)
    
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)
        
    serializer.save()
    
    return Response({
        "status": "ok",
        "data": serializer.data
    }, status=201)
    
@api_view(["PATCH"])
def update_user_view(request, user_id):
    try:
        user = UserProfile.objects.get(id = user_id)
    except UserProfile.DoesNotExist:
        return Response({
            "status": "error",
            "message": "User not found"
        }, status=404)
    
    serializer = UserProfileSerializer(user, data = request.data, partial=True)
    
    if not serializer.is_valid():
        return Response({
            "status": "error",
            "errors": serializer.errors
        }, status=400)
        
    serializer.save()
    
    return Response({
        "status": "ok",
        "data": serializer.data
    }, status=200)
    
@api_view(["DELETE"])
def delete_user_view(request, user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
    except UserProfile.DoesNotExist:
        return Response({
            "status": "error",
            "message": "User not found"
        }, status=404)
        
    user.delete()
    
    return Response({
        "status": "ok",
        "message": "User deleted"
    }, status=200)