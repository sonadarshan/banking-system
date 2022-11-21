from django.urls import path, include, re_path
from .views import UserRegistrationView, LogoutView, UserLoginView, CompleteRegistrationView


app_name = 'accounts'

urlpatterns = [
    # re_path('^verification/$', confirmation()),
    path(
        "login/", UserLoginView.as_view(),
        name="user_login"
    ),
    path(
        "logout/", LogoutView.as_view(),
        name="user_logout"
    ),
    path(
        "register/", UserRegistrationView.as_view(),
        name="user_registration"
    ),
    path(
        "complete_registration/", CompleteRegistrationView.as_view(),
        name="complete_registration"
    ),
]
