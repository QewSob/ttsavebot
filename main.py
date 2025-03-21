import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from yt_dlp import YoutubeDL
from pydub import AudioSegment  # Для конвертации в MP3

# Укажи полный путь к ffmpeg
AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"  # Для Windows
# Или
# AudioSegment.converter = "/usr/bin/ffmpeg"  # Для Linux/macOS

# Токен бота
TOKEN = '7671217981:AAGWQLgRH9mRN8OFIAYkajh5MImuxEUeSx4' # Токен берется из переменных окружения

# Функция для обработки команды /start
async def start(update: Update, context):
    await update.message.reply_text(
        'Привет! Я могу скачивать видео и конвертировать их в MP3 с различных платформ.\n'
        'Просто отправь мне ссылку на видео (TikTok, YouTube, Instagram и другие).'
    )

# Функция для скачивания видео и конвертации в MP3
async def download_video(update: Update, context):
    url = update.message.text
    chat_id = update.message.chat_id

    # Проверяем, что это ссылка
    if not url.startswith(('http://', 'https://')):
        await update.message.reply_text('Пожалуйста, отправь корректную ссылку на видео.')
        return

    # Определяем платформу
    if 'tiktok.com' in url:
        platform = 'TikTok'
    elif 'youtube.com' in url or 'youtu.be' in url:
        platform = 'YouTube'
    elif 'instagram.com' in url:
        platform = 'Instagram'
    else:
        platform = 'другой платформы'

    await update.message.reply_text(f'Скачиваю видео с {platform}...')

    # Настройки для yt-dlp
    ydl_opts = {
         'cookiefile': 'cookies.txt',  # Указываем файл с куками
        'format': 'best',  # Скачиваем лучшее качество
        'outtmpl': 'downloaded_video.mp4',  # Имя файла
        'noplaylist': True,  # Только одно видео
        'socket_timeout': 60,  # Таймаут
        'proxy': os.getenv('PROXY'),  # Используем прокси (если нужно)
        'http_headers': {  # Имитируем мобильный запрос
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.tiktok.com/',
        },
    }

    try:
        # Скачиваем видео
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Конвертируем видео в MP3
        await update.message.reply_text('Конвертирую видео в MP3...')
        video = AudioSegment.from_file("downloaded_video.mp4", format="mp4")
        video.export("converted_audio.mp3", format="mp3")

        # Отправляем видео пользователю
        with open('downloaded_video.mp4', 'rb') as video_file:
            await context.bot.send_video(chat_id=chat_id, video=video_file)

        # Отправляем аудио пользователю
        with open('converted_audio.mp3', 'rb') as audio_file:
            await context.bot.send_audio(chat_id=chat_id, audio=audio_file)

        # Удаляем временные файлы
        os.remove('downloaded_video.mp4')
        os.remove('converted_audio.mp3')
    except Exception as e:
        await update.message.reply_text(f'Произошла ошибка: {e}')

# Основная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Обработчики команд и сообщений
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
