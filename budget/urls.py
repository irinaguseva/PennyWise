from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BalanceView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("balance/", BalanceView.as_view(), name="balance"),
    path("categories/", include("categories.urls")),
    path("transactions/", include("transactions.urls")),
]
