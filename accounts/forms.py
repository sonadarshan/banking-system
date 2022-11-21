from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from captcha.fields import CaptchaField
from .models import User, BankAccountType, UserBankAccount, UserAddress
from .constants import GENDER_CHOICE


class UserLoginForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ["email", "password"]
    
    
class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(
        queryset=BankAccountType.objects.all(),
        widget=forms.Select(attrs={'placeholder': 'Gender', 'style': 'margin: 5px;padding: 10px;width: 100%;font-size: 17px;font-family: Raleway;border: 1px solid #aaaaaa;'}),
        empty_label="Select Acount Type"
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICE, widget=forms.Select(attrs={'placeholder': 'Gender', 'style': 'margin: 5px;padding: 10px;width: 100%;font-size: 17px;font-family: Raleway;border: 1px solid #aaaaaa;'}))
    birth_date = forms.DateField()
    passport = forms.CharField()
    signature = forms.ImageField()
    street_address = forms.CharField()
    city = forms.CharField()
    postal_code = forms.IntegerField()
    country = forms.CharField()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 '
                    'rounded py-3 px-4 leading-tight '
                    'focus:outline-none focus:bg-white '
                    'focus:border-gray-500'
                )
            })

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            account_type = self.cleaned_data.get('account_type')
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            passport = self.cleaned_data.get('passport')
            signature = self.cleaned_data.get('signature')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')
            postal_code = self.cleaned_data.get('postal_code')
            UserAddress.objects.create(
                user=user,
                street_address=street_address,
                city=city,
                country=country,
                postal_code=postal_code,
            )
            UserBankAccount.objects.create(
                user=user,
                gender=gender,
                birth_date=birth_date,
                account_type=account_type,
                passport=passport,
                signature = signature,
                account_no=(
                    user.id +
                    settings.ACCOUNT_NUMBER_START_FROM
                )
            )
        return user
