from django.urls import path
from . import views

urlpatterns = [
    path('channel/<str:name>/', views.ChannelWithStatsView.as_view(), name='channel-stats'),
    path('employee-kpi/', views.EmployeeKPIView.as_view(), name="employye-kpi"),
    path("<int:channel_id>/yearly-stats/", views.ChannelYearlyStatsAPIView.as_view(), name="channel-yearly-stats"),
    path("<int:channel_id>/stats-by-social-network/", views.ChannelStatsBySocialNetworkAPIView.as_view(), name="channel-stats-by-social-network"),
    path("channels/<int:channel_id>/social-stats/", views.ChannelSocialStatsView.as_view(), name="channel-social-stats"),
]