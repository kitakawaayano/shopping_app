from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        # DBのaccountsにも追加
        from shoppings.models import Accounts
        user = form.save()
        Accounts.objects.create(
            account_name=user.username,
            point = 0,
            admin = 0
        )
        return super().form_valid(form)
