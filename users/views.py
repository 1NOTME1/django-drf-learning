from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializer import UserInputSerializer, UserProfileSerializer

@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.all()
    result = {
        "status": "ok",
        "data": [],
        "count": 0
    }
    serializer = UserProfileSerializer(users, many = True)
    min_age = request.query_params.get("min_age")
    is_adult_param = request.query_params.get("is_adult")
    ordering = request.query_params.get("ordering")
    
        
    try:
        min_age = int(min_age)
    except (TypeError, ValueError):
        min_age = None
    
    if is_adult_param == "true":
        is_adult_filter = True
    elif is_adult_param == "false":
        is_adult_filter = False
    else:
        is_adult_filter = None
    
    for item in serializer.data:
        name = item["name"]
        age = item["age"]
        
        if not isinstance(age, int):
            continue
            
        if min_age is not None and age < min_age:
            continue
        
        if is_adult_filter is not None and (age >= 18) != is_adult_filter:
            continue
        
        result["data"].append({"name": name, "age": age, "is_adult": age >= 18})
        result["count"] += 1
    
    if ordering == "age":
        result["data"] = sorted(result["data"], key=lambda x : x["age"])
    elif ordering == "-age":
        result["data"] = sorted(result["data"], key=lambda x: x["age"], reverse=True)
    
    return Response(result)

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