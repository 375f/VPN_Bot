"""
Основной файл бота для управления VPN через Outline API.
"""
import os
import logging
import asyncio
import socket
from datetime import datetime, timedelta

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from config import Config
from api.outline import OutlineAPI
from handlers import admin, user

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='vpn_bot.log',  # Добавлен файл для логов
    filemode='a'
)

# Вывод логов также в консоль
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

# Периодическое сбрасывание счетчиков запросов (раз в сутки)
async def reset_request_counters():
    """Периодически сбрасывает счетчики запросов для всех пользователей."""
    while True:
        try:
            await asyncio.sleep(86400)  # 24 часа
            OutlineAPI.reset_limits()
        except Exception as e:
            logger.error(f"Ошибка при сбросе счетчиков: {str(e)}")

async def main():
    """Основная функция запуска бота."""
    # Проверка конфигурации
    if not Config.validate():
        logger.error("Не все обязательные переменные окружения заданы!")
        return
    
    # Инициализация бота и диспетчера
    bot = Bot(
        token=Config.TELEGRAM_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    try:
        # Регистрация роутеров обработчиков
        dp.include_router(admin.router)
        dp.include_router(user.router)
        
        # Установка команд бота
        await bot.set_my_commands([
            types.BotCommand(command="start", description="Открыть меню управления")
        ])
        
        # Передаем бот-объект в контекст для обработчиков
        # Это решение проблемы с доступом к боту в обработчиках для отправки сообщений
        dp.workflow_data["bot"] = bot
        
        # Запуск задачи сброса счетчиков запросов
        asyncio.create_task(reset_request_counters())
        
        # Запуск бота
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
    
    finally:
        # Корректное завершение работы
        logger.info("Завершение работы бота...")
        await OutlineAPI.close()
        await bot.session.close()

if __name__ == '__main__':
    try:
        # Проверка подключения к интернету
        socket.gethostbyname("api.telegram.org")
        logger.info("Проверка подключения успешна")
        
        # Запуск бота
        asyncio.run(main())
    
    except socket.gaierror:
        logger.error("Нет подключения к интернету!")
    
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    
    except Exception as e:
        logger.error(f"Фатальная ошибка: {str(e)}")