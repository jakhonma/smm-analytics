# app/admin.py
from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ChannelSocialStats
from .resources import ChannelSocialStatsResource
from django_admin_listfilter_dropdown.filters import RelatedDropdownFilter
from rangefilter.filters import NumericRangeFilter
from django.utils.translation import gettext_lazy as _


@admin.register(ChannelSocialStats)
class ChannelSocialStatsAdmin(ImportExportModelAdmin):
    resource_class = ChannelSocialStatsResource
    list_display = (
        "get_channel",
        "get_social_network",
        "get_employee",
        "year",
        "month",
        "views",
        "followers",
        "content_count",
    )
    list_filter = (
        ("year", NumericRangeFilter),
        ("month", NumericRangeFilter),
        ("smm_staff__channel_social_account", RelatedDropdownFilter),  # dropdown bo‘ladi
        # ("smm_staff__channel_social_account__channel", RelatedDropdownFilter),  # dropdown bo‘ladi
        # ("smm_staff__channel_social_account__social_network", RelatedDropdownFilter),  # dropdown bo‘ladi
    )
    # list_filter = (YearMonthInputFilter, "smm_staff__channel_social_account__social_network")
    search_fields = ("smm_staff__employee__full_name", "smm_staff__channel_social_account__channel__name")

    def get_channel(self, obj):
        return obj.smm_staff.channel_social_account.channel.name if obj.smm_staff else "-"
    get_channel.short_description = "Channel"

    def get_social_network(self, obj):
        return obj.smm_staff.channel_social_account.social_network.name if obj.smm_staff else "-"
    get_social_network.short_description = "Social Network"

    def get_employee(self, obj):
        return obj.smm_staff.employee.full_name if obj.smm_staff else "-"
    get_employee.short_description = "Employee"

