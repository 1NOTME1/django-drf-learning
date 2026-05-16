from rest_framework.routers import DefaultRouter
from .views import (
    UserProfileViewSet,
    DepartmentViewSet,
)

router = DefaultRouter()
router.register("departments", DepartmentViewSet, basename="department")
router.register("users", UserProfileViewSet, basename="user")

urlpatterns = router.urls