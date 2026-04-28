from django.urls import path
from .views import users_list_view, get_user_view, create_user_view, update_user_view, delete_user_view

urlpatterns = [
    path("users/", users_list_view),
    path("create/", create_user_view),
    path("user/<int:user_id>", get_user_view),
    path("update/<int:user_id>", update_user_view),
    path("delete/<int:user_id>", delete_user_view),
]