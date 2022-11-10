from django.urls import path

from .views import DepositMoneyView, TransactionReportView, LoansView, ProfileView


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("loans/", LoansView.as_view(), name="loans"),
]
