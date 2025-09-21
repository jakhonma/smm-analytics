from rest_framework import generics
from .serializers import UserSerializer
from django.contrib.auth.models import User


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
