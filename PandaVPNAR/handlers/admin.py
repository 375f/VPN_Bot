"""
Обработчики сообщений и колбэков для администраторов.
"""
import logging
from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from config import Config, Messages
from api.outline import OutlineAPI
from states.forms import Form
from keyboards.inline import (
    main_menu_keyboard, 
    keys_list_keyboard, 
    key_detail_keyboard,
    delete_confirmation_keyboard
)
from utils.decorators import admin_only, log_errors

# Создаем роутер для администраторских команд
router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(F.data == "create_key")
@admin_only
@log_errors
async def create_key_handler(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик запроса на создание ключа."""
    await callback.message.answer(Messages.ENTER_PORT)
    await state.set_state(Form.CREATE_PORT)
    await callback.answer()

@router.message(Form.CREATE_PORT)
@log_errors
async def process_port(message: types.Message, state: FSMContext):
    """Обработчик ввода номера порта."""
    if not message.text.isdigit():
        return await message.answer(Messages.ONLY_DIGITS)
    
    await state.update_data(port=int(message.text))
    await message.answer(Messages.ENTER_KEY_NAME)
    await state.set_state(Form.CREATE_NAME)

@router.message(Form.CREATE_NAME)
@log_errors
async def process_name(message: types.Message, state: FSMContext):
    """Обработчик ввода имени ключа."""
    data = await state.get_data()
    result = await OutlineAPI.create_key(data['port'], message.text)
    
    if result:
        await message.answer(
            Messages.KEY_CREATED.format(
                name=message.text,
                port=data['port'],
                url=result['accessUrl']
            ),
            reply_markup=await main_menu_keyboard(message.from_user.id)
        )
    else:
        await message.answer(
            Messages.KEY_CREATION_ERROR,
            reply_markup=await main_menu_keyboard(message.from_user.id)
        )
    
    await state.clear()

@router.callback_query(F.data == "list_keys")
@admin_only
@log_errors
async def list_keys_handler(callback: types.CallbackQuery):
    """Обработчик запроса на получение списка ключей."""
    keys = await OutlineAPI.get_all_keys()
    
    if not keys or 'accessKeys' not in keys or len(keys['accessKeys']) == 0:
        return await callback.answer(Messages.NO_KEYS_FOUND, show_alert=True)
    
    await callback.message.edit_text(
        Messages.KEY_LIST_TITLE,
        reply_markup=keys_list_keyboard(keys['accessKeys'])
    )
    await callback.answer()

@router.callback_query(F.data.startswith("key_detail_"))
@admin_only
@log_errors
async def key_detail_handler(callback: types.CallbackQuery):
    """Обработчик запроса детальной информации о ключе."""
    key_id = callback.data.split("_")[2]
    keys = await OutlineAPI.get_all_keys()
    
    if not keys or 'accessKeys' not in keys:
        return await callback.answer(Messages.NO_KEYS_FOUND, show_alert=True)
    
    key = next((k for k in keys['accessKeys'] if k['id'] == key_id), None)
    if not key:
        return await callback.answer(Messages.NO_KEYS_FOUND, show_alert=True)
    
    await callback.message.edit_text(
        Messages.KEY_DETAILS.format(
            id=key['id'],
            name=key.get('name', 'Без имени'),
            port=key['port'],
            url=key['accessUrl']
        ),
        reply_markup=key_detail_keyboard(key_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("delete_ask_"))
@admin_only
@log_errors
async def delete_ask_handler(callback: types.CallbackQuery):
    """Обработчик запроса на подтверждение удаления ключа."""
    key_id = callback.data.split("_")[2]
    
    await callback.message.edit_text(
        Messages.DELETE_CONFIRMATION,
        reply_markup=delete_confirmation_keyboard(key_id)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("delete_confirm_"))
@admin_only
@log_errors
async def delete_confirm_handler(callback: types.CallbackQuery):
    """Обработчик подтверждения удаления ключа."""
    key_id = callback.data.split("_")[2]
    
    if await OutlineAPI.delete_key(key_id):
        await callback.message.edit_text(
            Messages.KEY_DELETED,
            reply_markup=await main_menu_keyboard(callback.from_user.id)
        )
    else:
        await callback.answer(Messages.DELETE_ERROR, show_alert=True)