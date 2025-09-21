from django.contrib import admin
from .models import Employee, SMMStaff


@admin.register(SMMStaff)
class SMMStaffAdmin(admin.ModelAdmin):
    list_display = ["employee", "channel_social_account"]
    list_filter = ["channel_social_account__channel", "channel_social_account__social_network"]
    search_fields = ["employee__first_name", "employee__last_name"]


admin.site.register([Employee])
