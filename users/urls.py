from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UsersAPIView,
    UserDetailAPIView,
    DepartmentViewSet
    
)

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")

urlpatterns = [
    path("users/", UsersAPIView.as_view()),
    path("users/<int:user_id>/", UserDetailAPIView.as_view()),
]

urlpatterns += router.urls