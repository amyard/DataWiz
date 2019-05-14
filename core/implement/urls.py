from django.urls import path
from core.implement.views import MainPageView

urlpatterns = [
    path('', MainPageView.as_view(), name='base-view'),
]