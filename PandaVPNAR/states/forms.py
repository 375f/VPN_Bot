"""
Определение состояний для FSM (Finite State Machine).
"""
from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    """Состояния для формы создания ключа и обработки запросов."""
    # Создание ключа
    CREATE_PORT = State()
    CREATE_NAME = State()
    
    # Удаление ключа
    DELETE_CONFIRM = State()
    
    # Запрос ключа обычным пользователем
    TICKET_REQUEST = State()