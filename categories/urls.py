from django.urls import include, path
from rest_framework.routers import DefaultRouter

from budget.views import CategoryTotalView, CategoryViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")

urlpatterns = [
    path(
        "total/<str:category>/", CategoryTotalView.as_view(), name="specific-category"
    ),
] + router.urls
