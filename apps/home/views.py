from rest_framework import generics, response
from apps.analytic.models import ChannelSocialStats
from django.db.models import Sum, F
from .serializers import MainStatsSerializer, ChaertStatsSerializer
from .query import get_stats_by_network, get_social_networks_present_in_stats



class MainStatsView(generics.ListAPIView):
    serializer_class = MainStatsSerializer

    def get_queryset(self):
        return (
            ChannelSocialStats.objects
            .values(
                "channel_social_account__social_network__name",
                "channel_social_account__social_network__icon",
            )
            .annotate(
                social_network=F("channel_social_account__social_network__name"),
                social_network_icon=F("channel_social_account__social_network__icon"),
                total_views=Sum("views"),
                total_followers=Sum("followers"),
                total_content=Sum("content_count"),
            ).order_by("social_network")[:4]
        )


class ChartStatsView(generics.GenericAPIView):
    serializer_class = ChaertStatsSerializer

    def get(self, request, *args, **kwargs):
        get_social_networks_present_in_stats()

        data = get_stats_by_network()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)
