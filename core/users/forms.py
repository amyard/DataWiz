from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


User = get_user_model()



class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином не существует.')
        return username


    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data['password']
        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError('Невалидный пароль для данного пользователя.')
        elif not User.objects.get(username=username).check_password(password):
            raise forms.ValidationError('Неправильрный пароль.')
        return password



class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, UserCreationForm):
    username = forms.CharField(label='Пользователь', widget=forms.TextInput())
    email = forms.CharField(label='Електронная почта', widget=forms.EmailInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username


    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Ваши пароли не совпадают.')
        if len(password2) < 4:
            raise forms.ValidationError('Пароль должен быть не менее 4 символов')
        return password2


    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError('Пропустили символ @ в адресе електронной почты.')
        if '.' not in email:
            raise forms.ValidationError('Пропустили символ . в адресе електронной почты.')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Вы не можете использовать данный пароль.')

        try:
            mt = validate_email(email)
        except:
            raise forms.ValidationError('Incorrect email.')
        return email