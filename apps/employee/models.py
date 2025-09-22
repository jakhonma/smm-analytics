from django.db import models
from apps.channel.models import ChannelSocialAccount


class Employee(models.Model):
    """Xodimlar"""
    full_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar = models.ImageField(upload_to='employee_avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.full_name}"


class SMMStaff(models.Model):
    """Kanal ijtimoiy tarmoqlari uchun SMM xodimlar"""
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='smm_staffs')
    channel_social_account = models.ForeignKey(ChannelSocialAccount, on_delete=models.CASCADE, related_name='staff')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['employee', 'channel_social_account'],
                name='unique_employee_channel_social_account'
            )
        ]

    def __str__(self):
        return f"{self.employee} → {self.channel_social_account}"
