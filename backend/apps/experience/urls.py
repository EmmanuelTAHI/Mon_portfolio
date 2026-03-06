from rest_framework.routers import DefaultRouter

from .views import ExperienceViewSet

router = DefaultRouter()
router.register("", ExperienceViewSet, basename="experience")

urlpatterns = router.urls

