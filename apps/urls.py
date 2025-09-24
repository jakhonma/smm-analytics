from django.urls import path, include

urlpatterns = [
    path('auth/', include('apps.authentication.urls')),
    path('home/', include('apps.home.urls')),
    path('channel/', include('apps.channel.urls')),
    path('analytic/', include('apps.analytic.urls')),
]
