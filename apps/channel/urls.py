from django.urls import path
from .views import ChannelLestView 

urlpatterns = [
    path('channels/', ChannelLestView.as_view(), name='channel-list'),
]