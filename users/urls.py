from django.urls import path
from .views import users_list_view

urlpatterns = [
    path("users/", users_list_view),
]