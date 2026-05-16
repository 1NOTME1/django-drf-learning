from django.urls import path
from .views import (
    UsersAPIView,
    UserDetailAPIView,
    DepartmentsAPIView
    
)

urlpatterns = [
    path("users/", UsersAPIView.as_view()),
    path("users/<int:user_id>/", UserDetailAPIView.as_view()),
    path("departments/", DepartmentsAPIView.as_view()),
]
