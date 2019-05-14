from core.users.views import *
from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('base-view')), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
