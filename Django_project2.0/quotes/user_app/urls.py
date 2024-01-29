from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView

from .views import RegisterView, ResetPasswordView

app_name = "user_app"

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(template_name='user_app/login.html'), name='signin'),
    path('logout/', LogoutView.as_view(template_name='user_app/logout.html'), name='logout'),
    path('reset-password/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='user_app/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='user_app/password_reset_confirm.html',
                                          success_url='/user/reset-password/complete/'),
         name='password_reset_confirm'),
    path('reset-password/complete/',
         PasswordResetCompleteView.as_view(template_name='user_app/password_reset_complete.html'),
         name='password_reset_complete'),
]