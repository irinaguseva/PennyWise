from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, TransactionViewSet, BalanceView, CategoryReportView

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"transactions", TransactionViewSet, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("balance/", BalanceView.as_view(), name="balance"),
    path('report/categories/', CategoryReportView.as_view(), name='category-report'),
]
