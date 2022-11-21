import datetime

from django import forms
from django.conf import settings
from accounts.models import UserBankAccount
from .models import Transaction


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'to_account_no',
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):

    def clean_to_account_no(self):
        to_account_no =  self.cleaned_data.get('to_account_no')
        if to_account_no == self.account.account_no:
            raise forms.ValidationError(
                f'{to_account_no} is your account number !!!, Please enter other account number'
            )
        if not UserBankAccount.objects.filter(account_no=to_account_no).exists():
            raise forms.ValidationError(
                'Invalid Account Number, Please Enter the correct account number'
            )
        return to_account_no

    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} RM'
            )
        return amount

class RequestFundsForm(forms.Form):
    amount = forms.IntegerField(required=True)


class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")
        print(daterange)

        try:
            daterange = daterange.split(' - ')
            print(daterange)
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("Please select a date range.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("Invalid date range")
