"""
Файл конфигурации бота для управления VPN через Outline API.
"""
import os
from typing import Final
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Класс конфигурации приложения."""
    
    # API URL и токены
    OUTLINE_API_URL: Final[str] = os.getenv("OUTLINE_API_URL", "")
    OUTLINE_API_TOKEN: Final[str] = os.getenv("OUTLINE_API_TOKEN", "")
    TELEGRAM_TOKEN: Final[str] = os.getenv("TELEGRAM_TOKEN", "")
    
    # ID администратора
    ADMIN_ID: Final[int] = int(os.getenv("ADMIN_ID", 0))
    
    # Ограничения
    REQUEST_LIMIT: Final[int] = int(os.getenv("REQUEST_LIMIT", 3))
    
    # Проверка на валидность конфигурации
    @classmethod
    def validate(cls) -> bool:
        """Проверяет, что все необходимые переменные окружения заданы."""
        return all([
            cls.OUTLINE_API_URL, 
            cls.OUTLINE_API_TOKEN, 
            cls.TELEGRAM_TOKEN, 
            cls.ADMIN_ID
        ])

# Сообщения для пользователей
class Messages:
    """Тексты сообщений для бота."""
    
    WELCOME: Final[str] = "🔑 VPN Менеджер"
    ACCESS_DENIED: Final[str] = "🚫 Доступ запрещен!"
    ENTER_PORT: Final[str] = "Введите номер порта:"
    ONLY_DIGITS: Final[str] = "❌ Только числа!"
    ENTER_KEY_NAME: Final[str] = "Введите имя ключа:"
    KEY_CREATED: Final[str] = "✅ Ключ создан!\n🔐 Имя: {name}\n🔢 Порт: {port}\n📎 Ссылка: <code>{url}</code>"
    KEY_CREATION_ERROR: Final[str] = "❌ Ошибка создания!"
    NO_KEYS_FOUND: Final[str] = "❌ Ключи не найдены"
    KEY_LIST_TITLE: Final[str] = "📋 Список ключей:"
    KEY_DETAILS: Final[str] = (
        "🔐 Детали ключа:\n\n"
        "🆔 ID: {id}\n"
        "📛 Имя: {name}\n"
        "🔢 Порт: {port}\n"
        "📎 Ссылка: <code>{url}</code>"
    )
    DELETE_CONFIRMATION: Final[str] = "⚠️ Вы уверены, что хотите удалить ключ?"
    KEY_DELETED: Final[str] = "✅ Ключ успешно удален!"
    DELETE_ERROR: Final[str] = "❌ Ошибка удаления!"
    REQUEST_LIMIT_EXCEEDED: Final[str] = "🚫 Превышен лимит запросов!"
    DESCRIBE_REQUEST: Final[str] = "✍️ Опишите ваш запрос:"
    NEW_REQUEST: Final[str] = (
        "🆕 Новый запрос от @{username}\n"
        "👤 ID: {user_id}\n"
        "📝 Текст: {text}\n"
        "🕒 Время: {time}"
    )
    REQUEST_SENT: Final[str] = "✅ Ваш запрос отправлен администратору!"
    REQUEST_ERROR: Final[str] = "❌ Не удалось отправить запрос!"
    GENERIC_ERROR: Final[str] = "❌ Произошла ошибка!"