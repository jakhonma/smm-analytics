from rest_framework import serializers


class SocialDataSerializer(serializers.Serializer):
    channel = serializers.CharField()
    social_network = serializers.CharField()
    score = serializers.IntegerField()


class EmployeeStatsSerializer(serializers.Serializer):
    employee = serializers.CharField()
    avatar = serializers.URLField(allow_null=True, required=False)
    data = SocialDataSerializer(many=True)
    total_score = serializers.IntegerField()
    kpi = serializers.IntegerField()
