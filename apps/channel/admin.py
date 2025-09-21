from django.contrib import admin
from .models import Channel, SocialNetwork, ChannelSocialAccount

@admin.register(ChannelSocialAccount)
class ChannelSocialAccountAdmin(admin.ModelAdmin):
    list_display = ['channel', 'social_network', 'username', 'url']
    list_filter = ['channel', 'social_network']
    search_fields = ['channel__name', 'social_network__name', 'username']

admin.site.register([Channel, SocialNetwork])
