from django.db import models
from apps.employee.models import SMMStaff
from apps.channel.models import ChannelSocialAccount
from .validators import validate_year, validate_month, validate_not_future_year_month


class ChannelSocialStats(models.Model):
    """Har oy uchun statistik ma’lumotlar"""
    smm_staff = models.ForeignKey(
        to=SMMStaff, 
        on_delete=models.CASCADE, 
        related_name='monthly_stats'
    )
    channel_social_account = models.ForeignKey(
        to=ChannelSocialAccount,
        on_delete=models.SET_NULL,
        editable=True,
        null=True,
        blank=True,
        related_name='monthly_stats'
    )
    year = models.PositiveIntegerField(validators=[validate_year])
    month = models.PositiveIntegerField(validators=[validate_month])
    views = models.PositiveIntegerField(default=0)
    followers = models.PositiveIntegerField(default=0)
    content_count = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['smm_staff', 'year', 'month'],
                name='unique_staff_year_month'
            )
        ]
        ordering = ['-year', '-month']
    
    def clean(self):
        validate_not_future_year_month(self.year, self.month)
        return super().clean()
    
    def save(self, *args, **kwargs):
        # smm_staff orqali channel_social_account avtomatik set qilinadi
        if self.smm_staff and not self.channel_social_account:
            self.channel_social_account = self.smm_staff.channel_social_account
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.smm_staff} → {self.year}-{self.month}"



