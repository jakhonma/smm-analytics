from django.urls import path
from .views import ChannelWithStatsView, EmployeeKPIView, ChannelYearlyStatsAPIView

urlpatterns = [
    path('channel/<str:name>/', ChannelWithStatsView.as_view(), name='channel-stats'),
    path('employee-kpi/', EmployeeKPIView.as_view(), name="employye-kpi"),
    path("channels/<int:channel_id>/yearly-stats/", ChannelYearlyStatsAPIView.as_view(), name="channel-yearly-stats"),
]