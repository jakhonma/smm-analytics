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


#SOCIAL NETWORKLAR BO'YICHA FOIZ KO'RSATKICHLARINI HISOBLASH UCHUN QUERY
class StatsSerializer(serializers.Serializer):
    sum = serializers.IntegerField()
    instagram = serializers.IntegerField(default=0)
    facebook = serializers.IntegerField(default=0)
    youTube = serializers.IntegerField(default=0)
    telegram = serializers.IntegerField(default=0)


class SocialStatsSerializer(serializers.Serializer):
    views = StatsSerializer()
    followers = StatsSerializer()
    content = StatsSerializer()


#TOP 5 KANAL UCHUN SERIALIZER
class TopFiveChannelStatsSerializer(serializers.Serializer):
    channel_name = serializers.CharField(source="channel_social_account__channel__name")
    employee = serializers.CharField(source="smm_staff__employee__full_name")
    avatar = serializers.SerializerMethodField()
    final_score = serializers.FloatField()

    def get_avatar(self, obj):
        request = self.context.get("request")
        avatar_path = obj.get("smm_staff__employee__avatar")  # .values() dan keladigan string
        if avatar_path:
            return request.build_absolute_uri(f"{settings.MEDIA_URL}{avatar_path}")
        return None


#SOCIAL NETWORK RANKING UCHUN SERIALIZER
class SocialNetworkRankingSerializer(serializers.Serializer):
    name = serializers.CharField(source="channel_social_account__social_network__name")
    icon_path = serializers.SerializerMethodField()
    final_score = serializers.FloatField()

    def get_icon_path(self, obj):
        request = self.context.get("request")
        icon_path = obj.get("channel_social_account__social_network__icon")

        if icon_path and request:
            return request.build_absolute_uri(settings.MEDIA_URL + str(icon_path))
        return icon_path
