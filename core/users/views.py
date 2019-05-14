from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.views import LogoutView
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from django.views.generic import View, CreateView
from django.urls import reverse_lazy

from core.users.forms import CustomAuthenticationForm, CustomUserCreationForm

from bootstrap_modal_forms.generic import BSModalLoginView, BSModalCreateView



class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super(CustomLogoutView, self).get_next_page()
        messages.add_message(self.request, messages.SUCCESS, 'You successfully log out!')
        return next_page




class CustomLoginView(BSModalLoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('base-view')




class SignUpView(BSModalCreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/signup.html'
    success_message = 'Success: Sign up succeeded. You can now Log in.'
    success_url = reverse_lazy('base-view')

    def form_valid(self, form):
        form.instance.pass_for_api = form.cleaned_data['password1']
        return super(SignUpView, self).form_valid(form)