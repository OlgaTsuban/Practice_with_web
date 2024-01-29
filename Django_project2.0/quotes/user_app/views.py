from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import RegisterForm

# Create your views here.
class RegisterView(View):
    template_name = 'user_app/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="authors_app:all_authors")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Congratulations {username}. Your account was succsessfully  created !")
            return redirect(to="user_app:signin")
        return render(request, self.template_name, {"form": form})
    

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'user_app/password_reset.html'
    email_template_name = 'user_app/password_reset_email.html'
    html_email_template_name = 'user_app/password_reset_email.html'
    success_url = reverse_lazy('user_app:password_reset_done')
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'user_app/password_reset_subject.txt'
