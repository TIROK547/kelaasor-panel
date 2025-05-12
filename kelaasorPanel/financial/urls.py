from django.urls import path
from .views import (
    CreatePaymentView, ListAllFactorsView, ListUnpaidFactorsView,
    ListAllPaymentsView, ListUnpaidPaymentsView, DecidePaymentStateView
)

urlpatterns = [
    path("new/", CreatePaymentView.as_view()),
    path("admin/all-factors", ListAllFactorsView.as_view()),
    path("admin/unpaid-factors", ListUnpaidFactorsView.as_view()),
    path("admin/all-payments", ListAllPaymentsView.as_view()),
    path("admin/pending-payments", ListUnpaidPaymentsView.as_view()),
    path("admin/decide/<int:pk>", DecidePaymentStateView.as_view()),
]