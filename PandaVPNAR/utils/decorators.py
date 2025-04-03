"""
Вспомогательные декораторы для бота.
"""
import logging
from functools import wraps
from typing import Callable, Any, Awaitable

from aiogram import types
from aiogram.types import Message, CallbackQuery

from config import Config

logger = logging.getLogger(__name__)

def admin_only(func: Callable[[Any, Any], Awaitable[Any]]) -> Callable[[Any, Any], Awaitable[Any]]:
    """
    Декоратор для проверки, что пользователь является администратором.
    
    Args:
        func: Декорируемая функция
        
    Returns:
        Callable: Обернутая функция
    """
    @wraps(func)
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs) -> Any:
        user_id = event.from_user.id
        
        if user_id != Config.ADMIN_ID:
            if isinstance(event, CallbackQuery):
                await event.answer("🚫 Доступ запрещен!", show_alert=True)
                return None
            else:
                await event.answer("🚫 Доступ запрещен!")
                return None
                
        return await func(event, *args, **kwargs)
    
    return wrapper

def log_errors(func: Callable[[Any, Any], Awaitable[Any]]) -> Callable[[Any, Any], Awaitable[Any]]:
    """
    Декоратор для логирования ошибок в обработчиках.
    
    Args:
        func: Декорируемая функция
        
    Returns:
        Callable: Обернутая функция
    """
    @wraps(func)
    async def wrapper(event: Message | CallbackQuery, *args, **kwargs) -> Any:
        try:
            return await func(event, *args, **kwargs)
        except Exception as e:
            # Определение типа события
            if isinstance(event, Message):
                user_info = f"user_id={event.from_user.id}, chat_id={event.chat.id}"
                event_info = f"message_id={event.message_id}, text={event.text}"
            else:  # CallbackQuery
                user_info = f"user_id={event.from_user.id}, chat_id={event.message.chat.id}"
                event_info = f"callback_data={event.data}"
            
            logger.error(f"Ошибка в обработчике {func.__name__}: {str(e)}. {user_info}, {event_info}")
            
            # Отправка сообщения об ошибке пользователю
            try:
                if isinstance(event, Message):
                    await event.answer("❌ Произошла ошибка при обработке команды.")
                else:  # CallbackQuery
                    await event.answer("❌ Произошла ошибка!", show_alert=True)
            except Exception as send_error:
                logger.error(f"Не удалось отправить сообщение об ошибке: {str(send_error)}")
            
            return None
    
    return wrapper