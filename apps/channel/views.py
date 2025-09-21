from rest_framework import generics
from .models import Channel
from .serializers.channel import ChannelSerializer


class ChannelLestView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
