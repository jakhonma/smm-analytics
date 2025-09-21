from django.db import models
from apps.channel.models import ChannelSocialAccount


class Formula(models.Model):
    SOCIAL_METRICS = [
        ("content", "Content count"),
        ("views", "Views"),
        ("followers", "Followers"),
    ]
    channel_social_account = models.ForeignKey(
        to=ChannelSocialAccount, 
        on_delete=models.CASCADE,
        related_name='formulas'
    )
    metric = models.CharField(max_length=30, choices=SOCIAL_METRICS)
    min_value = models.PositiveIntegerField()
    points = models.PositiveIntegerField()

    class Meta:
        ordering = ["-min_value"]
    
    def __str__(self):
        return f"{self.channel_social_account} - {self.metric} -> {self.min_value} -> {self.points}"
