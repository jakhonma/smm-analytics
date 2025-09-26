from django.urls import path, include
from . import views


urlpatterns = [
    path('main-stats/', views.MainStatsView.as_view(), name='main-stats'),
    path('chart-stats/', views.ChartStatsView.as_view(), name='chart-stats'),
    path('main-social-stats/', views.MainSocialStatsView.as_view(), name='main-social-stats'),
    path('top-five-channels/', views.TopFiveChannelStatsView.as_view(), name='top-five-channels'),
    path('general-stats/', views.GeneralStatsView.as_view(), name='general-stats'),
    path('social-network-ranking/', views.SocialNetworkRankingView.as_view(), name='social-network-ranking'),
]
