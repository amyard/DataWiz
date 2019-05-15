from django.urls import path
from core.implement.views import MainPageView, CurrDateTableView

urlpatterns = [
    path('', MainPageView.as_view(), name='base-view'),
    path('curr-date-table/', CurrDateTableView.as_view(), name='curr-date-table')
]