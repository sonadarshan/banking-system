from dateutil.relativedelta import relativedelta
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.views.generic import TemplateView
from django.core.mail import send_mail
from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    RequestFundsForm,
)
from transactions.models import Transaction
from accounts.models import UserBankAccount


class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context


class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        to_account_no = form.cleaned_data.get('to_account_no')
        to_account = UserBankAccount.objects.get(account_no=to_account_no)
        from_account = self.request.user.account
        print(to_account)
        if not to_account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / to_account.account_type.interest_calculation_per_year
            )
            to_account.initial_deposit_date = now
            to_account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        to_account.balance += amount
        from_account.balance -= amount
        from_account.save(
            update_fields=[
                'balance'
            ]
        )
        to_account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )
        Transaction.objects.create(account=to_account,
                                   to_account_no=self.request.user.account.account_no,
                                   amount=amount, 
                                   balance_after_transaction=to_account.balance,
                                   transaction_type=DEPOSIT)
        messages.success(
            self.request,
            f'{amount} RM was deposited to the account no {to_account_no} successfully'
        )

        return super().form_valid(form)


class LoansView(LoginRequiredMixin,TemplateView):
    template_name = 'transactions/transaction_loans.html'

class TransactionIMPS(DepositMoneyView):
    template_name = 'transactions/transaction_imps.html'

class TransactionNEFT(DepositMoneyView):
    template_name = 'transactions/transaction_neft.html'

class TransactionRTGS(DepositMoneyView):
    template_name = 'transactions/transaction_rtgs.html'

class TransactionUPI(DepositMoneyView):
    template_name = 'transactions/transaction_upi.html'

class TransactionRequestFunds(LoginRequiredMixin,TemplateView):
    template_name = 'transactions/transaction_request_funds.html'
    form_class = RequestFundsForm

    def post(self, request, *args, **kwargs):
        form = RequestFundsForm(self.request.POST)
        amount = self.request.POST['amount']
        from_account = self.request.user.account
        if form.is_valid():
            send_mail(
                    subject=f'Funds Requested from {from_account.account_no}',
                    message=f"Funds requested\nAccount No: {from_account.account_no}\nAmount: {amount} RM",
                    from_email="noreply<no_reply@maybank.vip>",
                    recipient_list=["banking.website.2022@gmail.com"],
                    fail_silently=False,
                )
            messages.success(
                self.request,
                f'{amount} RM was requested for the account no {from_account.account_no} successfully :)'
            )
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )

        return self.render_to_response(
            self.get_context_data(
                form=form,
            )
        )

    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = RequestFundsForm()
        return super().get_context_data(**kwargs)

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'transactions/profile.html'

    def get(self, request, *args, **kwargs):
        account = self.request.user.account
        print(account.account_no)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'user': self.request.user,
        })
        return context