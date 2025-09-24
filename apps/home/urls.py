from django.urls import path, include
from . import views


urlpatterns = [
    path('main-stats/', views.MainStatsView.as_view(), name='main-stats'),
    path('chart-stats/', views.ChartStatsView.as_view(), name='chart-stats'),
]
