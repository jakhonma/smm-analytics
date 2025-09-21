from rest_framework import serializers
from apps.analytic.serializers.channel import ChannelSocialStatsSerializer
from .models import SMMStaff


class SmmStaffSerializer(serializers.ModelSerializer):

    monthly_stats = ChannelSocialStatsSerializer(many=True)

    class Meta:
        model = SMMStaff
        fields = ['id', 'monthly_stats']
