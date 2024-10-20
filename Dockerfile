# Используйте официальный образ Python
FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Копируйте зависимости файлов в контейнер
COPY requirements.txt .
# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируйте весь проект в контейнер
COPY . .

# Укажите команду для запуска вашего FastAPI приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


