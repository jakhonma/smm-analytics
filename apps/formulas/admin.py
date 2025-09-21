from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Formula
from .resources import FormulaResource


@admin.register(Formula)
class FormulaAdmin(ImportExportModelAdmin):
    resource_class = FormulaResource
    list_display = (
        "channel_name",
        "social_network_name",
        "metric",
        "min_value",
        "points",
    )
    list_filter = ("metric", "channel_social_account__channel", "channel_social_account__social_network")
    search_fields = ("channel_social_account__channel__name", "channel_social_account__social_network__name")

    def channel_name(self, obj):
        return obj.channel_social_account.channel.name
    channel_name.short_description = "Channel"

    def social_network_name(self, obj):
        return obj.channel_social_account.social_network.name
    social_network_name.short_description = "Social Network"
