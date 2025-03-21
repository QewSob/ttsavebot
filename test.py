from telegram import Bot

TOKEN = "7671217981:AAGbPcgRKB67rqwUg_aktcPmaS_lTVs1JIo"
bot = Bot(TOKEN)

# Отключаем Webhook и очищаем очередь обновлений
bot.delete_webhook(drop_pending_updates=True)

print("Webhook удалён, обновления очищены.")
