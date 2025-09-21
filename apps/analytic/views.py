from rest_framework.generics import RetrieveAPIView
from django.db.models import OuterRef, Subquery, F, IntegerField, ExpressionWrapper, Prefetch
from django.db.models.functions import Coalesce
from apps.channel.models import Channel, ChannelSocialAccount
from apps.analytic.models import ChannelSocialStats
from .serializers import ChannelWithStatsSerializer


class ChannelWithStatsView(RetrieveAPIView):
    serializer_class = ChannelWithStatsSerializer
    queryset = Channel.objects.all()

    def get_queryset(self):
        latest_stats = ChannelSocialStats.objects.filter(
            channel_social_account=OuterRef("pk")
        ).order_by("-year", "-month")

        previous_stats = ChannelSocialStats.objects.filter(
            channel_social_account=OuterRef("pk")
        ).order_by("-year", "-month")[1:2]

        annotated_accounts = ChannelSocialAccount.objects.annotate(
            latest_views=Subquery(latest_stats.values("views")[:1]),
            prev_views=Subquery(previous_stats.values("views")),
            latest_followers=Subquery(latest_stats.values("followers")[:1]),
            prev_followers=Subquery(previous_stats.values("followers")),
            latest_content=Subquery(latest_stats.values("content_count")[:1]),
            prev_content=Subquery(previous_stats.values("content_count")),
        ).annotate(
            diff_views=ExpressionWrapper(
                Coalesce(F("latest_views"), 0) - Coalesce(F("prev_views"), 0),
                output_field=IntegerField(),
            ),
            diff_followers=ExpressionWrapper(
                Coalesce(F("latest_followers"), 0) - Coalesce(F("prev_followers"), 0),
                output_field=IntegerField(),
            ),
            diff_content=ExpressionWrapper(
                Coalesce(F("latest_content"), 0) - Coalesce(F("prev_content"), 0),
                output_field=IntegerField(),
            ),
        )

        return Channel.objects.prefetch_related(
            Prefetch("social_accounts", queryset=annotated_accounts)
        )
