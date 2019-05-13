from django.urls import path
from core.implement import views

urlpatterns = [
    path('', views.index, name='base-view'),
]