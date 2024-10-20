import secrets

# Генерация случайного ключа длиной 32 байта
secret_key = secrets.token_urlsafe(32)
print(f"Ваш SECRET_KEY: {secret_key}")
