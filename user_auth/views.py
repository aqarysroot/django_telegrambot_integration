from rest_framework import generics, status
from rest_framework.response import Response

from user_auth.serializers import UserRegistrationSerializer
from user_auth.models import User
from telegram_api.models import UserSubscription
from telegram_api.helper import generate_token


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        return serializer.save()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        UserSubscription.objects.create(user=user, subscription_token=generate_token())
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

