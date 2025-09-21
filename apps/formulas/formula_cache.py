from django.core.cache import cache
from collections import defaultdict
from .models import Formula

KPI_CACHE_KEY = "formula_cache"


class RedisFormulaCache:
    """Redis orqali Formula cache (har bir channel uchun alohida key saqlaydi)"""

    @staticmethod
    def _group_formulas(formulas) -> dict[int, dict[str, list[dict]]]:
        """
        Formulalarni account_id va metric bo‘yicha guruhlash.
        Har bir formula dict ko‘rinishda saqlanadi.
        """
        grouped = defaultdict(lambda: defaultdict(list))
        for row in formulas:
            account_id = row["channel_social_account_id"]
            grouped[account_id][row["metric"]].append({
                "min_value": row["min_value"],
                "points": row["points"]
            })
        return grouped

    def refresh(self) -> None:
        """
        Barcha formulaslarni Redis cache-ga yangilab yozadi.
        """
        formulas = (
            Formula.objects
            .values("channel_social_account_id", "metric", "min_value", "points")
            .order_by("-min_value")
        )

        grouped = self._group_formulas(formulas)

        # Bulk set_many bilan Redisga yozamiz
        cache_data = {
            f"{KPI_CACHE_KEY}:{account_id}": dict(metrics)
            for account_id, metrics in grouped.items()
        }
        cache.set_many(cache_data, timeout=None)

    def get_data(self, account_id: int) -> dict:
        """
        Muayyan channel account uchun KPI ma'lumotlarini olish.
        Agar cache bo‘sh bo‘lsa, bazadan olib qayta saqlaydi.
        """
        key = f"{KPI_CACHE_KEY}:{account_id}"
        data = cache.get(key)

        if not data:
            formulas = (
                Formula.objects
                .filter(channel_social_account_id=account_id)
                .values("channel_social_account_id", "metric", "min_value", "points")
                .order_by("-min_value")
            )
            grouped = self._group_formulas(formulas)
            data = dict(grouped.get(account_id, {}))
            cache.set(key, data, timeout=None)

        return data
