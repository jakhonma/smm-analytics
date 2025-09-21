from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ChannelSocialStats
from .resources import ChannelSocialStatsResource


@admin.register(ChannelSocialStats)
class ChannelSocialStatsAdmin(ImportExportModelAdmin):
    resource_class = ChannelSocialStatsResource
    list_display = (
        "get_employee_full_name",
        "get_channel_name",
        "get_social_network_name",
        "year",
        "month",
        "views",
        "followers",
        "content_count",
    )
    list_filter = ("year", "month", "channel_social_account__channel", "channel_social_account__social_network")
    search_fields = ("smm_staff__employee__full_name",)

    def get_employee_full_name(self, obj):
        if obj.smm_staff and obj.smm_staff.employee:
            emp = obj.smm_staff.employee
            return f"{emp.full_name}"
        return "-"
    get_employee_full_name.short_description = "Employee Full Name"

    def get_channel_name(self, obj):
        return obj.channel_social_account.channel.name if obj.channel_social_account else "-"
    get_channel_name.short_description = "Channel"

    def get_social_network_name(self, obj):
        return obj.channel_social_account.social_network.name if obj.channel_social_account else "-"
    get_social_network_name.short_description = "Social Network"
