"""
Inline-клавиатуры для бота.
"""
from typing import List, Optional

from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config

async def is_admin(user_id: int) -> bool:
    """
    Проверяет, является ли пользователь администратором.
    
    Args:
        user_id (int): ID пользователя
        
    Returns:
        bool: True если пользователь администратор, иначе False
    """
    return user_id == Config.ADMIN_ID

async def main_menu_keyboard(user_id: int) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру главного меню в зависимости от прав пользователя.
    
    Args:
        user_id (int): ID пользователя
        
    Returns:
        types.InlineKeyboardMarkup: Клавиатура главного меню
    """
    builder = InlineKeyboardBuilder()
    
    if await is_admin(user_id):
        builder.row(
            types.InlineKeyboardButton(text="🆕 Создать ключ", callback_data="create_key"),
            types.InlineKeyboardButton(text="📋 Список ключей", callback_data="list_keys")
        )
    else:
        builder.add(types.InlineKeyboardButton(
            text="📨 Запросить ключ", 
            callback_data="request_key"
        ))
    
    return builder.as_markup()

def keys_list_keyboard(keys: List[dict]) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру со списком ключей.
    
    Args:
        keys (List[dict]): Список словарей с информацией о ключах
        
    Returns:
        types.InlineKeyboardMarkup: Клавиатура со списком ключей
    """
    builder = InlineKeyboardBuilder()
    
    for key in keys:
        builder.row(types.InlineKeyboardButton(
            text=f"🔑 {key.get('name', 'Без имени')}",
            callback_data=f"key_detail_{key['id']}"
        ))
    
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu"))
    return builder.as_markup()

def key_detail_keyboard(key_id: str) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру для детальной информации о ключе.
    
    Args:
        key_id (str): ID ключа
        
    Returns:
        types.InlineKeyboardMarkup: Клавиатура действий для ключа
    """
    builder = InlineKeyboardBuilder()
    
    builder.row(types.InlineKeyboardButton(
        text="🗑 Удалить ключ",
        callback_data=f"delete_ask_{key_id}"
    ))
    
    builder.row(types.InlineKeyboardButton(text="🔙 Назад", callback_data="list_keys"))
    return builder.as_markup()

def delete_confirmation_keyboard(key_id: str) -> types.InlineKeyboardMarkup:
    """
    Создает клавиатуру подтверждения удаления ключа.
    
    Args:
        key_id (str): ID ключа
        
    Returns:
        types.InlineKeyboardMarkup: Клавиатура подтверждения
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(text="✅ Да", callback_data=f"delete_confirm_{key_id}"),
        types.InlineKeyboardButton(text="❌ Нет", callback_data=f"key_detail_{key_id}")
    )
    return builder.as_markup()