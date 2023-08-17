from rest_framework import serializers
from user_auth.models import User
from telegram_api.models import UserSubscription

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            password=validated_data.pop('password'),
            **validated_data
        )

        return user
