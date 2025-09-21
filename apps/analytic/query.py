from django.db.models import Sum, Case, When, IntegerField, Value, Q
from .models import ChannelSocialStats
from collections import defaultdict
import datetime
from dateutil.relativedelta import relativedelta


# def employee_kpi_data():
#     today = datetime.date.today()
#     this_year, this_month = today.year, today.month

#     # Oldingi oy
#     if this_month == 1:
#         prev_year, prev_month = this_year - 1, 12
#     else:
#         prev_year, prev_month = this_year, this_month - 1

#     stats = (
#         ChannelSocialStats.objects.filter(
#             (Q(year=this_year, month=this_month) | Q(year=prev_year, month=prev_month))
#         )
#         .values(
#             "smm_staff__employee_id",
#             "smm_staff__employee__first_name",
#             "smm_staff__employee__last_name",
#             "channel_social_account__channel__name",
#             "channel_social_account__social_network__name",
#         )
#         .annotate(
#             this_views=Sum(
#                 Case(
#                     When(year=this_year, month=this_month, then="views"),
#                     default=Value(0),
#                     output_field=IntegerField(),
#                 )
#             ),
#             prev_views=Sum(
#                 Case(
#                     When(year=prev_year, month=prev_month, then="views"),
#                     default=Value(0),
#                     output_field=IntegerField(),
#                 )
#             ),
#             this_followers=Sum(
#                 Case(
#                     When(year=this_year, month=this_month, then="followers"),
#                     default=Value(0),
#                     output_field=IntegerField(),
#                 )
#             ),
#             prev_followers=Sum(
#                 Case(
#                     When(year=prev_year, month=prev_month, then="followers"),
#                     default=Value(0),
#                     output_field=IntegerField(),
#                 )
#             ),
#             content=Sum(
#                 Case(
#                     When(year=this_year, month=this_month, then="content_count"),
#                     default=Value(0),
#                     output_field=IntegerField(),
#                 )
#             ),
#             # prev_content=Sum(
#             #     Case(
#             #         When(year=prev_year, month=prev_month, then="content_count"),
#             #         default=Value(0),
#             #         output_field=IntegerField(),
#             #     )
#             # ),
#         )
#     )

#     # Dictionaryga yig‘ish
#     employees_data = defaultdict(lambda: {"employee": None, "channels": defaultdict(list)})

#     for row in stats:
#         emp_id = row["smm_staff__employee_id"]

#         # Employee fullname
#         employees_data[emp_id]["employee"] = (
#             f"{row['smm_staff__employee__first_name']} {row['smm_staff__employee__last_name']}"
#         )

#         channel = row["channel_social_account__channel__name"]

#         employees_data[emp_id]["channels"][channel].append({
#             "network": row["channel_social_account__social_network__name"],
#             "current": {
#                 "views": row["this_views"],
#                 "followers": row["this_followers"],
#                 "content": row["content"],
#             },
#             "prev": {
#                 "views": row["prev_views"],
#                 "followers": row["prev_followers"],
#                 # "content": row["prev_content"],
#             },
#         })

#     # Convert defaultdict to normal dict for JSON
#     result = []
#     for emp_id, data in employees_data.items():
#         result.append({
#             "employee_id": emp_id,
#             "employee": data["employee"],
#             "channels": [
#                 {
#                     "name": channel,
#                     "social_networks": social_networks
#                 }
#                 for channel, social_networks in data["channels"].items()
#             ],
#         })
#     return result


def employee_kpi_data():
    today = datetime.date.today()
    this_year, this_month = today.year, today.month

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
            channel_social_account__channel_id=channel_id,
            year__gte=start_date.year,
        )
        .filter(
            # faqat kerakli oylar oralig‘i
            (Q(year=start_date.year, month__gte=start_date.month)) |
            (Q(year=today.year, month__lte=today.month))
        )
        .values(
            "channel_social_account__social_network__id",
            "channel_social_account__social_network__name",
            "year",
            "month"
        )
        .annotate(
            total_views=Sum("views"),
            total_followers=Sum("followers"),
            total_content=Sum("content_count"),
        )
        .order_by("channel_social_account__social_network__id", "year", "month")
    )

    # Chart uchun tayyorlash
    data = {}
    for row in qs:
        sn_name = row["channel_social_account__social_network__name"]
        if sn_name not in data:
            data[sn_name] = {"views": [], "followers": [], "content": []}

        month_label = f"{row['year']}-{row['month']:02d}"

        data[sn_name]["views"].append({"month": month_label, "value": row["total_views"]})
        data[sn_name]["followers"].append({"month": month_label, "value": row["total_followers"]})
        data[sn_name]["content"].append({"month": month_label, "value": row["total_content"]})

    return data
