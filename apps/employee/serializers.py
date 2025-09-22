from rest_framework import serializers
from apps.analytic.serializers.channel import ChannelSocialStatsSerializer
from .models import SMMStaff


class SmmStaffSerializer(serializers.ModelSerializer):

    monthly_stats = ChannelSocialStatsSerializer(many=True)

    class Meta:
        model = SMMStaff
        fields = ['id', 'monthly_stats']


class SmmStaffEmployeesSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='employee.full_name')
    avatar = serializers.ImageField(source='employee.avatar')
    social_network = serializers.CharField(source='channel_social_account.social_network')

    class Meta:
        model = SMMStaff
        fields = ("id", "full_name", "avatar", 'social_network')

