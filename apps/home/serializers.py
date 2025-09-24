from rest_framework import serializers
from django.conf import settings


class MainStatsSerializer(serializers.Serializer):
    social_network = serializers.CharField()
    icon_path = serializers.SerializerMethodField()
    total_views = serializers.IntegerField()
    total_followers = serializers.IntegerField()
    total_content = serializers.IntegerField()

    def get_icon_path(self, obj):
        request = self.context.get("request")
        icon_path = obj.get("social_network_icon")

        if icon_path and request:
            return request.build_absolute_uri(settings.MEDIA_URL + str(icon_path))
        return icon_path


class ChartRowSerializer(serializers.Serializer):
    name = serializers.CharField()
    Telegram = serializers.IntegerField(required=False, default=0)
    Instagram = serializers.IntegerField(required=False, default=0)
    Facebook = serializers.IntegerField(required=False, default=0)
    YouTube = serializers.IntegerField(required=False, default=0)


class ChaertStatsSerializer(serializers.Serializer):
    views = ChartRowSerializer(many=True)
    followers = ChartRowSerializer(many=True)
    content = ChartRowSerializer(many=True)