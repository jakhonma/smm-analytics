# app/resources.py
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django.core.exceptions import ValidationError
from .models import ChannelSocialStats
from apps.channel.models import ChannelSocialAccount
from apps.employee.models import SMMStaff


class ChannelSocialStatsResource(resources.ModelResource):
    # Modelda mavjud bo‘lgan field (import uchun kerak)
    smm_staff = fields.Field(
        column_name="smm_staff",
        attribute="smm_staff",
        widget=ForeignKeyWidget(SMMStaff, "id"),
    )

    # Excel fayl ustunlari (export/import uchun)
    channel = fields.Field(column_name="channel", readonly=True)
    social_network = fields.Field(column_name="social_network", readonly=True)
    employee = fields.Field(column_name="employee", readonly=True)

    year = fields.Field(column_name="year", attribute="year")
    month = fields.Field(column_name="month", attribute="month")
    views = fields.Field(column_name="views", attribute="views")
    followers = fields.Field(column_name="followers", attribute="followers")
    content_count = fields.Field(column_name="content_count", attribute="content_count")

    class Meta:
        model = ChannelSocialStats
        fields = (
            "id",
            "smm_staff",
            "channel",
            "social_network",
            "employee",
            "year",
            "month",
            "views",
            "followers",
            "content_count",
        )
        export_order = (
            "id",
            "channel",
            "social_network",
            "employee",
            "year",
            "month",
            "views",
            "followers",
            "content_count",
        )

    # Export qilish uchun dehydrate metodlari
    def dehydrate_channel(self, obj):
        if getattr(obj, "smm_staff", None):
            return obj.smm_staff.channel_social_account.channel.name
        return ""

    def dehydrate_social_network(self, obj):
        if getattr(obj, "smm_staff", None):
            return obj.smm_staff.channel_social_account.social_network.name
        return ""

    def dehydrate_employee(self, obj):
        if getattr(obj, "smm_staff", None):
            return obj.smm_staff.employee.full_name
        return ""

    # Importdan oldin validatsiya
    def before_import_row(self, row, **kwargs):
        """
        Importdan oldin: Exceldagi channel + social_network + employee orqali
        SMMStaff topib, row['smm_staff'] ga id yozamiz.
        """
        channel_name = (row.get("channel") or "").strip()
        social_name = (row.get("social_network") or "").strip()
        employee_name = (row.get("employee") or "").strip()

        if not channel_name or not social_name or not employee_name:
            raise ValidationError("channel, social_network yoki employee ustuni bo'sh yoki noto'g'ri.")

        # ChannelSocialAccount topamiz
        try:
            channel_acc = ChannelSocialAccount.objects.get(
                channel__name=channel_name,
                social_network__name=social_name,
            )
        except ChannelSocialAccount.DoesNotExist:
            raise ValidationError(
                f"ChannelSocialAccount topilmadi: '{channel_name}' - '{social_name}'."
            )

        # SMMStaff topamiz
        try:
            smm_staff = SMMStaff.objects.get(
                channel_social_account=channel_acc,
                employee__full_name=employee_name,  # yoki employee__id agar ID bilan ishlatsangiz
            )
        except SMMStaff.DoesNotExist:
            raise ValidationError(
                f"SMMStaff topilmadi: {employee_name} → ({channel_name} - {social_name})."
            )

        # Import jarayonida modelga FK ni bog‘lab beramiz
        row["smm_staff"] = str(smm_staff.id)
