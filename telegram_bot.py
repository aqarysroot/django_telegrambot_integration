from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, CallbackContext, ApplicationBuilder
from telegram.ext import filters

import os
import django
import threading
from django.db import transaction

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from telegram_api.models import UserSubscription

# Set your Telegram bot token
TELEGRAM_BOT_TOKEN = '6660362103:AAGomMCuCvLxLZO77MZxR4z6JnJDcbe_i-k'

# Initialize the bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def update_user_subscription(token, chat_id):
    try:
        with transaction.atomic():
            user_subscription = UserSubscription.objects.select_for_update().get(subscription_token=token)
            user_subscription.chat_id = chat_id
            user_subscription.save()
    except UserSubscription.DoesNotExist:
        print("User subscription not found.")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome to the subscription service! Send /subscribe to start receiving messages.")

async def subscribe(update: Update, context: CallbackContext):

    args = context.args
    if len(args) != 1:
        await  update.message.reply_text("Usage: /subscribe <token>")
        return

    token = args[0]
    chat_id = update.message.chat_id

    # Check if the provided token is valid
    subscription_thread = threading.Thread(target=update_user_subscription, args=(token, chat_id))
    subscription_thread.start()
    await update.message.reply_text("You are now subscribed to receive messages.")

async def echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    message_text = update.message.text
    # Send the user's message back to the user
    await bot.send_message(chat_id=chat_id, text=f"You sent: {message_text}")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    subscribe_handler = CommandHandler("subscribe", subscribe)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(start_handler)
    application.add_handler(subscribe_handler)
    application.add_handler(echo_handler)

    application.run_polling()


if __name__ == '__main__':
    main()