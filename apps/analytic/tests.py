from django.test import TestCase

def kpi_percent(score: int) -> int:
    if score >= 95:
        return 100
    elif score >= 89:
        return 90
    elif score >= 84:
        return 80
    elif score >= 78:
        return 70
    elif score >= 72:
        return 60
    elif score >= 66:
        return 50
    elif score >= 60:
        return 40
    elif score >= 54:
        return 30
    elif score >= 48:
        return 20
    elif score >= 42:
        return 10
    return 0


# def kpi_percent(score: int) -> int:
#     thresholds = {
#         95: 100,
#         89: 90,
#         84: 80,
#         78: 70,
#         72: 60,
#         66: 50,
#         60: 40,
#         54: 30,
#         48: 20,
#         42: 10,
#     }
#     # Eng katta thresholdni tanlaydi, agar score >= threshold
#     result = thresholds.get(max((t for t in thresholds if score >= t), default=None), 0)
#     return result

print(kpi_percent(52))
