# from abc import ABC
# from .formula_cache import RedisFormulaCache


# class ChannelSocialAccountScore(ABC):
#     def __init__(self, cache: RedisFormulaCache, account_id: int):
#         self.cache = cache
#         self.account_id = account_id

#     def score_count(self, value: int, metric: str) -> int:
#         """Berilgan metric uchun qiymatni hisoblab, ball qaytaradi"""
#         rules = self.cache.get_data(self.account_id)
#         metric_rules = rules.get(metric, [])

#         if not metric_rules:
#             return 0

#         for rule in metric_rules:
#             if value >= rule.min_value:
#                 return rule.points

#         return 0


from .formula_cache import RedisFormulaCache


class ChannelSocialAccountScoreService:
    def __init__(self, cache: RedisFormulaCache):
        self.cache = cache

    def score_sum(self, account_id: int, values: list[int]) -> int:
        """
        values -> [views_value, followers_value, content_value]
        Har bir metric bo‘yicha ballarni hisoblab yig‘indisini qaytaradi
        """
        metrics = ["views", "followers", "content"]
        rules = self.cache.get_data(account_id)

        total_score = 0
        for metric, value in zip(metrics, values):
            metric_rules = rules.get(metric, [])
            if not metric_rules:
                continue

            for rule in metric_rules:
                if value >= rule["min_value"]:
                    total_score += rule["points"]
                    break  # eng katta mos keladiganini oldik

        return total_score

