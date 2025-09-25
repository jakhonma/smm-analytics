import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Q, Value, Case, When, FloatField, F, ExpressionWrapper
from apps.analytic.models import ChannelSocialStats
from django.db.models.functions import Coalesce


#12 OYLIK CHARTLARGA UCHUN VIEWS, FOLLOWERS, CONTENT MA'LUMOT OLISH QUERY
def get_stats_by_network():
    today = datetime.date.today()
    start_date = today - relativedelta(months=11)  # 12 oy (shu oy ham kiritilgan)

    qs = (
        ChannelSocialStats.objects
        .filter(
            year__gte=start_date.year,
        )
        .filter(
            (Q(year=start_date.year, month__gte=start_date.month)) |
            (Q(year=today.year, month__lte=today.month))
        )
        .values(
            "year",
            "month",
            "channel_social_account__social_network__name",
        )
        .annotate(
            total_views=Sum("views"),
            total_followers=Sum("followers"),
            total_content=Sum("content_count"),
        )
        .order_by("year", "month")
    )

    views_data, followers_data, content_data = {}, {}, {}

    for row in qs:
        month_label = f"{row['year']}-{row['month']:02d}"
        sn = row["channel_social_account__social_network__name"]

        # Views
        if month_label not in views_data:
            views_data[month_label] = {"name": month_label}
        views_data[month_label][sn] = row["total_views"] or 0

        # Followers
        if month_label not in followers_data:
            followers_data[month_label] = {"name": month_label}
        followers_data[month_label][sn] = row["total_followers"] or 0

        # Content
        if month_label not in content_data:
            content_data[month_label] = {"name": month_label}
        content_data[month_label][sn] = row["total_content"] or 0

    return {
        "views": list(views_data.values()),
        "followers": list(followers_data.values()),
        "content": list(content_data.values()),
    }


#SOCIAL NETWORKLAR BO'YICHA FOIZ KO'RSATKICHLARINI HISOBLASH UCHUN QUERY
def get_social_networks_present_in_stats():

    stats = (
        ChannelSocialStats.objects
        .values("channel_social_account__social_network__name")
        .annotate(
            total_views=Coalesce(Sum("views"), 0),
            total_followers=Coalesce(Sum("followers"), 0),
            total_content=Coalesce(Sum("content_count"), 0),
        )
    )

    result = {
        "views": {"sum": 0},
        "followers": {"sum": 0},
        "content": {"sum": 0},
    }

    for item in stats:
        name = str(item["channel_social_account__social_network__name"]).title().replace(" ", "").lower()

        # views
        result["views"]["sum"] += item["total_views"]
        result["views"][name] = item["total_views"]

        # followers
        result["followers"]["sum"] += item["total_followers"]
        result["followers"][name] = item["total_followers"]

        # content
        result["content"]["sum"] += item["total_content"]
        result["content"][name] = item["total_content"]
    return result


#TOP 5 KANAL UCHUN QUERY
def get_top_channels():
    base_stats = (
        ChannelSocialStats.objects
        .values(
            "channel_social_account__channel__name",
            "smm_staff__employee__full_name",
            "smm_staff__employee__avatar",
        )
        .annotate(
            views_sum=Coalesce(Sum("views"), 0),
            followers_sum=Coalesce(Sum("followers"), 0),
            content_sum=Coalesce(Sum("content_count"), 0),
        )
        .annotate(
            engagement=Case(
                When(followers_sum__gt=0, then=F("views_sum") * 1.0 / F("followers_sum")),
                default=Value(0.0),
                output_field=FloatField(),
            ),
            efficiency=Case(
                When(content_sum__gt=0, then=F("views_sum") * 1.0 / F("content_sum")),
                default=Value(0.0),
                output_field=FloatField(),
            ),
        )
        .annotate(
            raw_score=ExpressionWrapper(
                (F("engagement") * 0.5) + (F("efficiency") * 0.5),
                output_field=FloatField(),
            )
        )
    )

    # 2. Umumiy yig‘indi hisoblash
    total_score = base_stats.aggregate(total=Sum("raw_score"))["total"] or 1

    # 3. Foizga o‘tkazish
    stats = (
        base_stats
        .annotate(
            final_score=ExpressionWrapper(
                (F("raw_score") / total_score) * 100,
                output_field=FloatField(),
            )
        )
        .order_by("-final_score")
    )
    return stats