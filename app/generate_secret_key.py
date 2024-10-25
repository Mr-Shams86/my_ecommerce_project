import secrets

# Генерация случайного ключа длиной 32 байта
secret_key = secrets.token_urlsafe(32)

# Путь к файлу .env
env_file_path = '.env'

# Запись ключа в файл .env
with open(env_file_path, 'a') as env_file:
    env_file.write(f"SECRET_KEY={secret_key}\n")

print(f"Ваш SECRET_KEY: {secret_key}")
print(f"SECRET_KEY был записан в файл {env_file_path}. Пожалуйста, добавьте его в вашу конфигурацию.")