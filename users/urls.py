from django.urls import path
from .views import (
    UsersAPIView,
    get_user_view,
    update_user_view,
    delete_user_view,
    DepartmentsAPIView
    
)

urlpatterns = [
    path("users/", UsersAPIView.as_view()),
    path("users/<int:user_id>/", get_user_view),
    path("users/<int:user_id>/update/", update_user_view),
    path("users/<int:user_id>/delete/", delete_user_view),
    path("departments/", DepartmentsAPIView.as_view()),
]
