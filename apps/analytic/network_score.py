from abc import ABC
from ..formulas.formula_cache import RedisFormulaCache


class NetworkScore(ABC):
    def __init__(self, cache: RedisFormulaCache, network_name: str):
        self.cache = cache
        self.network_name = network_name

    def score_count(self, value, social_type):
        rules = self.cache.get_data()
        network_rules = rules.get(self.network_name, {})
        metric_rules = network_rules.get(social_type, [])
        min_value = 0
        for rule in metric_rules:
            if rule["min_value"] < value:
                min_value = rule["points"]
                break
        return min_value


class Instagram(NetworkScore):
    def __init__(self,  cache):
        super().__init__(cache, "Instagram")


class Telegram(NetworkScore):
    def __init__(self, cache):
        super().__init__(cache, "Telegram")


class Facebook(NetworkScore):
    def __init__(self, cache):
        super().__init__(cache, "Facebook")
