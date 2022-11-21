from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, RedirectView
from verify_email.email_handler import send_verification_email
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegistrationForm, UserLoginForm
from django.core.mail import send_mail


User = get_user_model()


class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_registration.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST, self.request.FILES)
        if registration_form.is_valid():
            user = registration_form.save()
            # address.save()
            user = send_verification_email(request, registration_form)
            messages.success(
                self.request,
                (
                    f'Please verify your email to login'
                )
            )
            send_mail(
                subject='Your Registered Account Details are',
                message=f'Name:{user.first_name} {user.last_name}\nAccount No:{user.account.account_no}\nEmail:{user.email}\nOnly after email verification, your account will be activated',
                from_email="noreply<no_reply@maybank.vip>",
                recipient_list=[self.request.POST['email']],
                fail_silently=False,
            )
            return HttpResponseRedirect(
                reverse_lazy('accounts:complete_registration')
            )
        else:
            print(registration_form.errors)

        return self.render_to_response(
            self.get_context_data(
                registration_form=registration_form,
            )
        )

    def get_context_data(self, **kwargs):
        print("Inside Get")
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        return super().get_context_data(**kwargs)



class UserLoginView(TemplateView):
    form_class = UserLoginForm
    template_name='accounts/user_login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        login_form = UserLoginForm(self.request.POST)
        email = self.request.POST['email']
        password = self.request.POST['password']
        user = authenticate(request, email=email, password=password)
        if login_form.is_valid():
            print("form valid")
        else:
            print("Invalid Form")
        if user is not None:
                login(self.request, user)
                messages.success(self.request,("Login Successful"))
                return HttpResponseRedirect(
                reverse_lazy('transactions:profile')
            )
        else:
            messages.error(self.request, ("Please Check your login details !!!!"))
            
        return self.render_to_response(
            self.get_context_data(
                login_form=login_form,
            )
        )

    def get_context_data(self, **kwargs):
        if 'login_form' not in kwargs:
            kwargs['login_form'] = UserLoginForm()
        return super().get_context_data(**kwargs)

class LogoutView(RedirectView):
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)

class CompleteRegistrationView(TemplateView):
    template_name= 'accounts/registration_complete.html'
    