# Используй официальный образ Python
FROM python:3.10-slim

# Установи ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Установи зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопируй код приложения
COPY . .

# Запусти приложение
CMD ["python", "main.py"]