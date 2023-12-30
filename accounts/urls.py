from django.contrib.auth.views import LogoutView
from django.urls import path, reverse_lazy
from .views import SignUp, EmailConfirmationSentView, UserConfirmEmailView, EmailConfirmedView, \
    EmailConfirmationFailedView, LoginView, logout_view

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('confirm-email/<str:uidb64>/<str:token>/', UserConfirmEmailView.as_view(), name='confirm_email'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('email-confirmation-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
    path('login/', LoginView.as_view(), name='login'),
]