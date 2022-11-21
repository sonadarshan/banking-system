from django.urls import path

from .views import DepositMoneyView, TransactionReportView, LoansView, ProfileView, TransactionIMPS, TransactionNEFT, TransactionRTGS, TransactionUPI, TransactionRequestFunds


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("loans/", LoansView.as_view(), name="loans"),
    path("money_transfer_imps/", TransactionIMPS.as_view(), name="money_transfer_imps"),
    path("money_transfer_neft/", TransactionNEFT.as_view(), name="money_transfer_neft"),
    path("money_transfer_rtgs/", TransactionRTGS.as_view(), name="money_transfer_rtgs"),
    path("money_transfer_upi/", TransactionUPI.as_view(), name="money_transfer_upi"),
    path("money_transfer_requestFunds/", TransactionRequestFunds.as_view(), name="money_transfer_request_funds"),
]
