from django.db.models import Sum, Case, When, IntegerField, Value, Q
from .models import ChannelSocialStats
from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta
from django.conf import settings


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
            Q(year=this_year, month=this_month) | Q(year=prev_year, month=prev_month)
        )
        .values(
            "smm_staff__employee_id",
            "smm_staff__employee__full_name",  # faqat full_name ishlatamiz
            "smm_staff__employee__avatar",
            "channel_social_account_id",
            "channel_social_account__channel__name",
            "channel_social_account__social_network__name",
        )
        .annotate(
            this_views=Sum(
                Case(
                    When(year=this_year, month=this_month, then="views"),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            prev_views=Sum(
                Case(
                    When(year=prev_year, month=prev_month, then="views"),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            this_followers=Sum(
                Case(
                    When(year=this_year, month=this_month, then="followers"),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            prev_followers=Sum(
                Case(
                    When(year=prev_year, month=prev_month, then="followers"),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
            content=Sum(
                Case(
                    When(year=this_year, month=this_month, then="content_count"),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ),
        )
    )

    employees_data = defaultdict(lambda: {"employee": None, "accounts": []})

    for row in stats:
        emp_id = row["smm_staff__employee_id"]

        # Endi faqat full_name
        employees_data[emp_id]["employee"] = row["smm_staff__employee__full_name"]
        
        avatar_path = row["smm_staff__employee__avatar"]
        if avatar_path:
            employees_data[emp_id]["avatar"] = request.build_absolute_uri(settings.MEDIA_URL + avatar_path)

        employees_data[emp_id]["accounts"].append({
            "id": row["channel_social_account_id"],
            "channel": row["channel_social_account__channel__name"],
            "social_network": row["channel_social_account__social_network__name"],
            "current": {
                "views": row["this_views"],
                "followers": row["this_followers"],
                "content": row["content"],
            },
            "prev": {
                "views": row["prev_views"],
                "followers": row["prev_followers"],
            },
        })


    return [
        {
            "employee_id": emp_id,
            "employee": data["employee"],
            "avatar": data.get("avatar"),
            "accounts": data["accounts"],
        }
        for emp_id, data in employees_data.items()
    ]


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
