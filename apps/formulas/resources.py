from import_export import resources, fields
from import_export.widgets import Widget
from .models import Formula
from apps.channel.models import ChannelSocialAccount


class ChannelSocialAccountWidget(Widget):
    """
    Channel va Social Network ustunlari orqali ChannelSocialAccount ni topib beradi.
    """
    def clean(self, value, row=None, *args, **kwargs):
        channel_name = row.get("channel_name") or row.get("Channel")   # Fayldagi ustun nomiga qarab moslashadi
        social_network_name = row.get("social_network_name") or row.get("Social Network")

        if not channel_name or not social_network_name:
            raise ValueError("Excel faylda Channel yoki Social Network ustuni yo‘q!")

        try:
            return ChannelSocialAccount.objects.get(
                channel__name=channel_name.strip(),
                social_network__name=social_network_name.strip()
            )
        except ChannelSocialAccount.DoesNotExist:
            raise ValueError(
                f"ChannelSocialAccount topilmadi: {channel_name} / {social_network_name}"
            )

    def render(self, value, obj=None):
        if value:
            return f"{value.channel.name} | {value.social_network.name}"
        return ""


class FormulaResource(resources.ModelResource):
    # Excelda ishlatadigan ustunlar
    channel_name = fields.Field(
        column_name="channel_name",  # Excel fayl nomi shu bo‘lsa ishlaydi
        attribute="channel_social_account",
        widget=ChannelSocialAccountWidget()
    )
    social_network_name = fields.Field(
        column_name="social_network_name",  # Excel fayl nomi shu bo‘lsa ishlaydi
        attribute="channel_social_account",
        widget=ChannelSocialAccountWidget()
    )

    class Meta:
        model = Formula
        fields = (
            "id",
            "channel_name",
            "social_network_name",
            "metric",
            "min_value",
            "points",
        )
        export_order = (
            "id",
            "channel_name",
            "social_network_name",
            "metric",
            "min_value",
            "points",
        )

    def dehydrate_channel_name(self, formula: Formula):
        return formula.channel_social_account.channel.name

    def dehydrate_social_network_name(self, formula: Formula):
        return formula.channel_social_account.social_network.name
