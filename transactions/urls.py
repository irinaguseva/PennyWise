from django.urls import path
from rest_framework.routers import DefaultRouter

from budget.views import (BalanceView, CategoryReportView,
                          FinancialRecommendationView, ReportDownloadView)
from .views.transaction import TransactionViewSet

router = DefaultRouter()
router.register(r"", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("recommendation/", FinancialRecommendationView.as_view(), name="financial-recommendation"),
    path("report/", CategoryReportView.as_view(), name="specific-category"),
    path("balance/", BalanceView.as_view(), name="balance"),
    path('download/', ReportDownloadView.as_view(), name='download_test_report'),
] + router.urls
