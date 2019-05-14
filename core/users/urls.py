from core.users.views import *
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('base-view')), name='logout'),
    path('signup/', RegistrationView.as_view(), name='signup'),
]
