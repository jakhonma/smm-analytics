from rest_framework import generics, response
from apps.analytic.models import ChannelSocialStats
from django.db.models import Sum, F
from .serializers import MainStatsSerializer, ChaertStatsSerializer, SocialStatsSerializer, TopFiveChannelStatsSerializer
from .query import get_stats_by_network, get_social_networks_present_in_stats, get_top_channels


#ASOSIY SOCIAL NETWORKLAR BO'YICHA UMUMIY KO'RSATKICHLAR
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


#ASOSIY UCHUN 12 OYLIK CHART UCHUN
class ChartStatsView(generics.GenericAPIView):
    serializer_class = ChaertStatsSerializer

    def get(self, request, *args, **kwargs):
        data = get_stats_by_network()
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)


#ASOSIY UCHUN SOCIAL NETWORKLARNI FOIYZ KO'RSATKICHLARI HISOBLASH UCHUN
class MainSocialStatsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        data = get_social_networks_present_in_stats()
        serializer = SocialStatsSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return response.Response(serializer.data)


#TOP 5 KANAL UCHUN
class TopFiveChannelStatsView(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        stats = get_top_channels()[:5]
        serializer = TopFiveChannelStatsSerializer(stats, many=True, context={'request': request})
        return response.Response(serializer.data)
