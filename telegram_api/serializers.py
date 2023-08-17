from rest_framework import serializers
from telegram_api.models import UserSubscription, UserMessage

class TelegramAPISerializer(serializers.Serializer):
    message = serializers.CharField()


class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserSubscription
        fields = ['subscription_token']


class UserMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMessage
        fields = ['message', 'time']
