from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import RegisterView

app_name = "user_app"

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(template_name='user_app/login.html'), name='signin'),
    path('logout/', LogoutView.as_view(template_name='user_app/logout.html'), name='logout'),
]