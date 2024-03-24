# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем зависимости проекта (requirements.txt)
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для Flask, чтобы указать, что приложение будет работать в режиме production
ENV FLASK_ENV=production

# Указываем порт, на котором будет работать Flask приложение
ENV FLASK_RUN_PORT=3000

# Указываем команду для запуска приложения (в данном случае, запускаем Flask-приложение)
CMD ["flask", "run", "--host=0.0.0.0"]
