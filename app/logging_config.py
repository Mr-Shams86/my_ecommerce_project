import logging
from logging.handlers import RotatingFileHandler

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # уровень логирования

# Создание обработчика для записи логов в файл с вращением
file_handler = RotatingFileHandler("app.log", maxBytes=10*1024*1024, backupCount=5)  # 10 MB
file_handler.setLevel(logging.DEBUG)  # Уровень логирования для файла

# Создание обработчика для вывода логов в консоль
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Уровень логирования для консоли

# Формат логирования
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Добавление обработчиков к логгеру
logger.addHandler(file_handler)
logger.addHandler(console_handler)
