from django.db import models
from user_auth.models import User


class UserSubscription(models.Model):
    chat_id = models.BigIntegerField(unique=True, null=True)
    subscription_token = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.chat_id)


class UserMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=1000)
    time = models.DateTimeField(auto_now_add=True)
