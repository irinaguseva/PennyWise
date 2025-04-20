from django.urls import include, path
from django_prometheus import exports
from rest_framework.routers import DefaultRouter

from .views import (BalanceView, CategoryReportView, CategoryTotalView,
                    CategoryViewSet, FinancialRecommendationView,
                    TransactionViewSet)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("balance/", BalanceView.as_view(), name="balance"),
    path("total/<str:category>/", CategoryTotalView.as_view(), name="specific-category"),
    path("report/", CategoryReportView.as_view(), name="specific-category"),
    path("recommendation/", FinancialRecommendationView.as_view(), name="financial-recommendation"),
    path('metrics/', exports.ExportToDjangoView),
]
