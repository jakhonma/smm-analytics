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


# from rest_framework import serializers
# from apps.employee.serializers import SmmStaffSerializer


# class EmployeeKPISerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     first_name = serializers.CharField(max_length=100)
#     last_name = serializers.CharField(max_length=100)
#     middle_name = serializers.CharField(max_length=100, required=False, allow_blank=True)
#     phone_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
#     smm_staffs = SmmStaffSerializer(many=True)
