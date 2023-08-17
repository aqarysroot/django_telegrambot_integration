import asyncio
from django.conf import settings
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from telegram import Bot
from telegram_api.serializers import TelegramAPISerializer, UserTokenSerializer, UserMessageSerializer
from telegram_api.models import UserSubscription, UserMessage
from telegram_api.helper import format_message


class TelegramAPIView(generics.GenericAPIView):
    serializer_class = TelegramAPISerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        UserMessage.objects.create(user=request.user, message=message)

        user_sub = UserSubscription.objects.filter(user=request.user).first()
        if user_sub is None:
            return Response({"message": "something went wrong"})

        # Forward the message to the Telegram bot
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        asyncio.run(bot.send_message(chat_id=user_sub.chat_id, text=format_message(request.user.first_name, message)))

        return Response({"message": "Message forwarded to bot."})


class TokenRetrieveView(generics.RetrieveAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return UserSubscription.objects.get(user=self.request.user)


class UserMessageListView(generics.ListAPIView):
    queryset = UserMessage.objects.all()
    serializer_class = UserMessageSerializer

    def get_queryset(self):
        return UserMessage.objects.filter(user=self.request.user)

