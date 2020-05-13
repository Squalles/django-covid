from rest_framework.routers import DefaultRouter

from stats.views import CountryViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename='country')
urlpatterns = router.urls
