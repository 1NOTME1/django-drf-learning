from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializer import UserInputSerializer

@api_view(["GET"])
def users_list_view(request):
    users = UserProfile.objects.all()
    result = {
    "status": "ok",
    "data": [],
    "count": 0
}
    serializer = UserInputSerializer(users, many = True)
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
