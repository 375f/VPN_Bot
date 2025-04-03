"""
Обработчики сообщений и колбэков для обычных пользователей.
"""
import logging
from datetime import datetime

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from config import Config, Messages
from api.outline import OutlineAPI
from states.forms import Form
from keyboards.inline import main_menu_keyboard
from utils.decorators import log_errors

# Создаем роутер для пользовательских команд
router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("start"))
@log_errors
async def cmd_start(message: types.Message):
    """Обработчик команды /start."""
    await message.answer(
        Messages.WELCOME,
        reply_markup=await main_menu_keyboard(message.from_user.id)
    )

@router.callback_query(F.data == "main_menu")
@log_errors
async def main_menu_handler(callback: types.CallbackQuery):
    """Обработчик возврата в главное меню."""
    await callback.message.edit_text(
        Messages.WELCOME,
        reply_markup=await main_menu_keyboard(callback.from_user.id)
    )
    await callback.answer()

@router.callback_query(F.data == "request_key")
@log_errors
async def request_key_handler(callback: types.CallbackQuery, state: FSMContext):
    """Обработчик запроса на получение ключа."""
    if not await OutlineAPI.check_limit(callback.from_user.id):
        await callback.answer(Messages.REQUEST_LIMIT_EXCEEDED, show_alert=True)
        return

    await callback.message.answer(Messages.DESCRIBE_REQUEST)
    await state.set_state(Form.TICKET_REQUEST)
    await callback.answer()

@router.message(Form.TICKET_REQUEST)
@log_errors
async def process_ticket_request(message: types.Message, state: FSMContext, bot):
    """Обработчик текста запроса на ключ."""
    try:
        # Формируем текст заявки
        request_text = Messages.NEW_REQUEST.format(
            username=message.from_user.username or f"user{message.from_user.id}",
            user_id=message.from_user.id,
            text=message.text,
            time=datetime.now().strftime('%d.%m.%Y %H:%M')
        )
        
        # Отправляем админу
        await bot.send_message(Config.ADMIN_ID, request_text)
        
        # Сообщаем пользователю
        await message.answer(
            Messages.REQUEST_SENT,
            reply_markup=await main_menu_keyboard(message.from_user.id)
        )
        
    except Exception as e:
        logger.error(f"Ошибка обработки запроса: {str(e)}")
        await message.answer(
            Messages.REQUEST_ERROR,
            reply_markup=await main_menu_keyboard(message.from_user.id)
        )
    
    finally:
        await state.clear()