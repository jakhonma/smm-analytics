from apps.formulas.services import ChannelSocialAccountScoreService
from .kpi_percent import kpi_percent


class KPIService:
    def __init__(self, data, service: ChannelSocialAccountScoreService):
        self.data = data
        self.service = service

    @staticmethod
    def get_points(value, rules):
        for rule in rules:
            if value >= rule["min_value"]:
                return rule["points"]
        return 0

    @staticmethod
    def calc_percentage(prev, current):
        if prev == 0:
            return 100 if current > 0 else 0
        return ((current - prev) / prev) * 100
    
    @staticmethod
    def calc_percentage2(prev, current):
        if prev == 0:
            return 100 if current > 0 else 0
        return (current / prev) * 100
    
    def evaluate(self):
        employees = []
        for emp in self.data:
            total_score = 0
            employee_result = {"employee": emp["employee"], "avatar": emp['avatar'], "data": [], 'total_score': 0, 'kpi': 0}
            for account in emp["accounts"]:
                score_sum = 0
                current = account["current"]
                prev = account["prev"]

                view_percentage = self.calc_percentage2(prev["views"], current["views"])
                follower_percentage = self.calc_percentage2(prev["followers"], current["followers"])
                values = [view_percentage, follower_percentage, current['content']]

                score_sum = self.service.score_sum(account_id=account['id'], values=values)
                total_score += score_sum
                employee_result["data"].append({
                    "channel": account['channel'],
                    "social_network": account["social_network"],
                    "score": score_sum
                })
            kpi_result = kpi_percent(total_score)
            employee_result['total_score'] = total_score
            employee_result["kpi"] = kpi_result
            employees.append(employee_result)
        return employees


    # def evaluate(self):
    #     employees = []
    #     for emp in self.data:
    #         total_score = 0
    #         employee_result = {"emp": emp["employee"], "channels": [], 'kpi': 0}
    #         for channel in emp["accounts"]:
    #             score_sum = 0
    #             networks = []
    #             for net in channel["social_networks"]:
    #                 net_name = net["network"].lower()
    #                 current = net["current"]
    #                 prev = net["prev"]

    #                 handler = self.networks.get(net_name)
    #                 if not handler:
    #                     continue

    #                 view_percentage = self.calc_percentage2(prev["views"], current["views"])
    #                 follower_percentage = self.calc_percentage2(prev["followers"], current["followers"])
    #                 view_score = handler.score_count(view_percentage, "views")
    #                 follower_score = handler.score_count(follower_percentage, "followers")
    #                 content_score = handler.score_count(current["content"], "content")
    #                 score_sum += view_score + follower_score + content_score
    #                 print(view_score, follower_score, content_score)
    #                 print(score_sum, 333333333)
    #             total_score += score_sum
    #             print(channel)
    #             employee_result["channels"].append({
    #                 "channel": channel['name'],
    #                 "networks": networks,
    #                 "score": score_sum
    #             })
    #         kpi_result = kpi_percent(total_score)
    #         employee_result["kpi"] = kpi_result
    #         employees.append(employee_result)
    #     return employees

