from django.urls import path
from .views import (
    users_list_view,
    get_user_view,
    create_user_view,
    update_user_view,
    delete_user_view,
    departments_list_view
)

urlpatterns = [
    path("users/", users_list_view),
    path("users/create/", create_user_view),
    path("users/<int:user_id>/", get_user_view),
    path("users/<int:user_id>/update/", update_user_view),
    path("users/<int:user_id>/delete/", delete_user_view),
    path("departments/", departments_list_view),
]
