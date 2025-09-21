from rest_framework import serializers
from apps.channel.models import Channel, SocialNetwork


class ChannelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    # logo = serializers.ImageField(required=False, allow_null=True)


class ChannelSocialAccountSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())
    social_network = serializers.PrimaryKeyRelatedField(queryset=SocialNetwork.objects.all())
    username = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=255)
    url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
