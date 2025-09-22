from django.db.models import Sum, Case, When, IntegerField, Value, Q, F
from .models import ChannelSocialStats
from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db.models.functions import Coalesce


from django.db.models import Sum, Q, IntegerField, Value
from collections import defaultdict
from django.conf import settings
import datetime


def employee_kpi_data(request, year=None, month=None):
    today = datetime.date.today()
    this_year = year or today.year
    this_month = month or today.month

    # Oldingi oy
    if this_month == 1:
        prev_year, prev_month = this_year - 1, 12
    else:
        prev_year, prev_month = this_year, this_month - 1

    stats = (
        ChannelSocialStats.objects.filter(
            Q(year=this_year, month=this_month) |
            Q(year=prev_year, month=prev_month)
        )
        .values(
            "smm_staff__employee_id",
            "smm_staff__employee__full_name",
            "smm_staff__employee__avatar",
            "channel_social_account_id",
            "channel_social_account__channel__name",
            "channel_social_account__social_network__name",
        )
        .annotate(
            this_views=Sum("views", filter=Q(year=this_year, month=this_month)),
            prev_views=Sum("views", filter=Q(year=prev_year, month=prev_month)),

            this_followers=Sum("followers", filter=Q(year=this_year, month=this_month)),
            prev_followers=Sum("followers", filter=Q(year=prev_year, month=prev_month)),

            content=Sum("content_count", filter=Q(year=this_year, month=this_month)),
        )
    )

    employees_data = {}

    for row in stats:
        emp_id = row["smm_staff__employee_id"]

        emp_data = employees_data.setdefault(emp_id, {
            "employee_id": emp_id,
            "employee": row["smm_staff__employee__full_name"],
            "avatar": None,
            "accounts": []
        })

        avatar_path = row["smm_staff__employee__avatar"]
        if avatar_path and not emp_data["avatar"]:  # birinchi marta qo‘shamiz
            emp_data["avatar"] = request.build_absolute_uri(settings.MEDIA_URL + avatar_path)

        emp_data["accounts"].append({
            "id": row["channel_social_account_id"],
            "channel": row["channel_social_account__channel__name"],
            "social_network": row["channel_social_account__social_network__name"],
            "current": {
                "views": row["this_views"] or 0,
                "followers": row["this_followers"] or 0,
                "content": row["content"] or 0,
            },
            "prev": {
                "views": row["prev_views"] or 0,
                "followers": row["prev_followers"] or 0,
            },
        })

    return list(employees_data.values())



def get_channel_last_one_year(channel_id):
    today = datetime.date.today()
    start_date = today - relativedelta(months=11)  # 12 oy oldin (hozirgi oyni ham qo‘shib)
    
    qs = (
        ChannelSocialStats.objects
        .filter(
            smm_staff__channel_social_account__channel_id=channel_id,
            year__gte=start_date.year,
        )
        .filter(
            # faqat kerakli oylar oralig‘i
            (Q(year=start_date.year, month__gte=start_date.month)) |
            (Q(year=today.year, month__lte=today.month))
        )
        .values(
            "smm_staff__channel_social_account__social_network__id",
            "smm_staff__channel_social_account__social_network__name",
            "year",
            "month",
            'smm_staff__employee__full_name',
            'smm_staff__employee__avatar',
        )
        .annotate(
            total_views=Sum("views"),
            total_followers=Sum("followers"),
            total_content=Sum("content_count"),
        )
        .order_by( "year", "month")
    )

    views_data, followers_data, content_data = {}, {}, {}
    employees = {}
    
    for row in qs:
        month_label = f"{row['year']}-{row['month']:02d}"
        sn = row["smm_staff__channel_social_account__social_network__name"]
        full_name = row['smm_staff__employee__full_name']
        avatar = row['smm_staff__employee__avatar']
        
        if full_name not in employees:
            employees[full_name] = {
                "full_name": full_name,
                "avatar": avatar,
                "social_networks": []
            }

        # social_network faqat unik bo‘lsin
        if sn not in employees[full_name]["social_networks"]:
            employees[full_name]["social_networks"].append(sn)

        # Views chart
        if month_label not in views_data:
            views_data[month_label] = {"name": month_label}
        views_data[month_label][sn] = row["total_views"] or 0

        # Followers chart
        if month_label not in followers_data:
            followers_data[month_label] = {"name": month_label}
        followers_data[month_label][sn] = row["total_followers"] or 0

        # Content chart
        if month_label not in content_data:
            content_data[month_label] = {"name": month_label}
        content_data[month_label][sn] = row["total_content"] or 0

    return {
        "employees": list(employees.values()),
        "views": list(views_data.values()),
        "followers": list(followers_data.values()),
        "content": list(content_data.values()),
    }


def channel_stats_by_social_network(channel_id: int):
    stats = (
        ChannelSocialStats.objects.filter(
            channel_social_account__channel_id=channel_id
        )
        .values(
            "channel_social_account__social_network__name",
        )
        .annotate(
            total_views=Sum("views"),
            total_followers=Sum("followers"),
            total_content=Sum("content_count"),
        )
        .order_by("channel_social_account__social_network__name")
    )

    return stats


def get_channel_social_stats(request, channel_id: int):
    today = datetime.date.today()
    this_year, this_month = today.year, today.month

    # Oldingi oy (year, month ni hisoblab chiqamiz)
    if this_month == 1:
        prev_year = this_year - 1
        prev_month = 12
    else:
        prev_year = this_year
        prev_month = this_month - 1

    qs = (
        ChannelSocialStats.objects.filter(channel_social_account__channel_id=channel_id)
        .values(
            "smm_staff__channel_social_account__social_network__name",
            "smm_staff__channel_social_account__social_network__icon",
        )
        .annotate(
            # Jami (total)
            total_views=Coalesce(Sum("views"), Value(0, output_field=IntegerField())),
            total_followers=Coalesce(Sum("followers"), Value(0, output_field=IntegerField())),
            total_content=Coalesce(Sum("content_count"), Value(0, output_field=IntegerField())),

            # O‘tgan oy
            prev_views=Coalesce(
                Sum("views", filter=Q(year=prev_year, month=prev_month)),
                Value(0, output_field=IntegerField())
            ),
            prev_followers=Coalesce(
                Sum("followers", filter=Q(year=prev_year, month=prev_month)),
                Value(0, output_field=IntegerField())
            ),
            prev_content=Coalesce(
                Sum("content_count", filter=Q(year=prev_year, month=prev_month)),
                Value(0, output_field=IntegerField())
            ),

            # Hozirgi oy
            curr_views=Coalesce(
                Sum("views", filter=Q(year=this_year, month=this_month)),
                Value(0, output_field=IntegerField())
            ),
            curr_followers=Coalesce(
                Sum("followers", filter=Q(year=this_year, month=this_month)),
                Value(0, output_field=IntegerField())
            ),
            curr_content=Coalesce(
                Sum("content_count", filter=Q(year=this_year, month=this_month)),
                Value(0, output_field=IntegerField())
            ),
        )
        .annotate(
            social_network=F("channel_social_account__social_network__name"),
            icon_path=F("channel_social_account__social_network__icon"),
            diff_views=F("curr_views") - F("prev_views"),
            diff_followers=F("curr_followers") - F("prev_followers"),
            diff_content=F("curr_content") - F("prev_content"),
        )
        .values(
            "social_network",
            "icon_path",
            "diff_views", "diff_followers", "diff_content",
            "total_views", "total_followers", "total_content",
        )
    )

    # Icon’ni to‘liq media yo‘l bilan qaytarish
    result = []
    for row in qs:
        icon = row["icon_path"]
        if icon:
            row["icon_path"] = (
                request.build_absolute_uri(settings.MEDIA_URL + str(row["icon_path"]))
            )
        result.append(row)

    return result
