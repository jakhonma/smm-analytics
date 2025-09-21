from import_export import resources, fields, widgets
from .models import ChannelSocialStats
from apps.channel.models import ChannelSocialAccount

# Custom ForeignKeyWidget
class SafeForeignKeyWidget(widgets.ForeignKeyWidget):
    def get_queryset(self, value, row, *args, **kwargs):
        """
        value bo'yicha filterlash, agar bir nechta yozuv topilsa,
        oxirgi (yoki birinchi) yozuvni qaytaradi
        """
        qs = super().get_queryset(value, row, *args, **kwargs)
        return qs

    def clean(self, value, row=None, *args, **kwargs):
        """
        get() o'rniga filter va first() ishlatamiz
        """
        if value is None:
            return None
        qs = self.get_queryset(value, row, *args, **kwargs).filter(**{self.field: value})
        obj = qs.first()  # birinchi mos yozuvni oladi
        if obj is None:
            raise widgets.WidgetValueError(f"{self.model.__name__} matching '{value}' not found.")
        return obj


class ChannelSocialStatsResource(resources.ModelResource):
    employee_full_name = fields.Field(
        column_name="Employee Full Name"
    )
    channel_name = fields.Field(
        column_name="Channel",
        attribute="channel_social_account",
        widget=SafeForeignKeyWidget(ChannelSocialAccount, "channel_social_account__channel__name")
    )
    social_network_name = fields.Field(
        column_name="Social Network",
        attribute="channel_social_account",
        widget=SafeForeignKeyWidget(ChannelSocialAccount, "channel_social_account__social_network__name")
    )

    class Meta:
        model = ChannelSocialStats
        fields = (
            "id",
            "employee_full_name",
            "channel_name",
            "social_network_name",
            "year",
            "month",
            "views",
            "followers",
            "content_count",
        )
        export_order = fields

    def dehydrate_employee_full_name(self, obj):
        # smm_staff hech qachon bo'sh bo'lmaydi
        return obj.smm_staff.employee.full_name
