from django.urls import path
from .views import ChannelLestView, ChannelEmployeesListView

urlpatterns = [
    path('channels/', ChannelLestView.as_view(), name='channel-list'),
    path("channels/<int:channel_id>/employees/", ChannelEmployeesListView.as_view(), name="channel-employees"),
]