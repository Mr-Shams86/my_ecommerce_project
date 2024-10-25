import os
from fastapi import UploadFile
from fastapi import HTTPException
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  
MEDIA_DIR = BASE_DIR / "media"  # Используем оператор / для создания пути

# Создаем директорию для хранения медиафайлов, если она не существует
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}

def allowed_file(filename: str) -> bool:
    """Проверяет, является ли файл допустимым изображением."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

async def save_file(file: UploadFile) -> str:
    """Сохраняет загруженный файл и возвращает его путь."""
    if not allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = MEDIA_DIR / file.filename  # Используем оператор / для создания пути

    # Сохраняем файл на диск
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return str(file_path)

def delete_file(file_path: str):
    """Удаляет файл из файловой системы."""
    if os.path.isfile(file_path):
        os.remove(file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

def get_file_path(filename: str) -> str:
    """Возвращает полный путь к файлу."""
    return str(MEDIA_DIR / filename)  # Используем оператор / для создания пути
