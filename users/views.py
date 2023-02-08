from django.contrib.auth import get_user_model
from django.views.generic import UpdateView

from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from allauth.account.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserChangeForm


class MyAccountPageView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    success_message = 'Update Successful'
    template_name = 'account/my_account.html'

    def get_object(self):
        return self.request.user


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('my-account')
