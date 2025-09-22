from rest_framework import generics, views
from .models import Channel
from .serializers.channel import ChannelSerializer
from apps.employee.serializers import SmmStaffSerializer, SmmStaffEmployeesSerializer
from apps.employee.models import SMMStaff


class ChannelLestView(generics.ListAPIView):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer


class ChannelEmployeesListView(generics.ListAPIView):
    serializer_class = SmmStaffEmployeesSerializer
    lookup_field = "channel_id"

    def get_queryset(self):
        channel_id = self.kwargs["channel_id"]
        return SMMStaff.objects.filter(
            channel_social_account__channel_id=channel_id
        ).distinct()
