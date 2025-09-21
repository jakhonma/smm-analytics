from django.db import models


class BaseModel(models.Model):
    """Asosiy model"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        abstract = True


class Channel(BaseModel):
    """Asosiy kanal (mahalla, telekanal)"""
    # logo = models.ImageField(upload_to='channel_logos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class SocialNetwork(BaseModel):
    """Ijtimoiy tarmoq turi (Instagram, Telegram, Facebook)"""
    score = models.PositiveSmallIntegerField(default=0)
    icon = models.ImageField(upload_to='social_network_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


class ChannelSocialAccount(models.Model):
    """Kanalning ijtimoiy tarmoqdagi akkaunti"""
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name='social_accounts')
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.channel.name} — {self.social_network.name}"
