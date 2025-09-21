from rest_framework import serializers
from apps.channel.models import Channel, ChannelSocialAccount

class ChannelSocialAccountStatsSerializer(serializers.ModelSerializer):
    social_network = serializers.CharField(source="social_network.name")
    icon = serializers.ImageField(source="social_network.icon", read_only=True)

    latest_views = serializers.IntegerField(read_only=True)
    prev_views = serializers.IntegerField(read_only=True)
    diff_views = serializers.IntegerField(read_only=True)

    latest_followers = serializers.IntegerField(read_only=True)
    prev_followers = serializers.IntegerField(read_only=True)
    diff_followers = serializers.IntegerField(read_only=True)

    latest_content = serializers.IntegerField(read_only=True)
    prev_content = serializers.IntegerField(read_only=True)
    diff_content = serializers.IntegerField(read_only=True)

    class Meta:
        model = ChannelSocialAccount
        fields = [
            "id",
            "social_network",
            "icon",
            "latest_views",
            "prev_views",
            "diff_views",
            "latest_followers",
            "prev_followers",
            "diff_followers",
            "latest_content",
            "prev_content",
            "diff_content",
        ]


class ChannelWithStatsSerializer(serializers.ModelSerializer):
    social_accounts = ChannelSocialAccountStatsSerializer(many=True, read_only=True)

    class Meta:
        model = Channel
        fields = ["id", "name", "social_accounts"]


class ChannelSocialStatsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    # channel_social_account = serializers.IntegerField(required=False, allow_null=True)
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    views = serializers.IntegerField(default=0)
    followers = serializers.IntegerField(default=0)
    content_count = serializers.IntegerField(default=0)
