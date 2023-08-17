from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from telegram_api.views import TelegramAPIView, TokenRetrieveView, UserMessageListView

app_name = 'telegram_api'

urlpatterns = [
    path('send/', TelegramAPIView.as_view(), name='user_registration'),
    path('token/', TokenRetrieveView.as_view(), name='user_token'),
    path('messages/', UserMessageListView.as_view(), name='user_token'),

]
