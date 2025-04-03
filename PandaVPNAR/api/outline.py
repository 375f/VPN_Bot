"""
API клиент для взаимодействия с Outline VPN API.
"""
import logging
from typing import Dict, Optional, Any, List

import aiohttp
from aiohttp.client_exceptions import ClientError

from config import Config

logger = logging.getLogger(__name__)

class OutlineAPI:
    """Класс для работы с API сервера Outline."""
    
    _session: Optional[aiohttp.ClientSession] = None
    _user_requests: Dict[int, int] = {}  # Счетчик запросов по user_id
    
    @classmethod
    async def get_session(cls) -> aiohttp.ClientSession:
        """
        Получение или создание aiohttp сессии.
        
        Returns:
            aiohttp.ClientSession: Активная сессия
        """
        if cls._session is None or cls._session.closed:
            # Подготовка URL API
            base_url = Config.OUTLINE_API_URL
            if not base_url.endswith('/'):
                base_url += '/'
                logger.warning("Автоматически добавлен / в конец URL")
                
            cls._session = aiohttp.ClientSession(
                base_url=base_url,
                headers={"Authorization": f"Bearer {Config.OUTLINE_API_TOKEN}"},
                connector=aiohttp.TCPConnector(ssl=False)
            )
        return cls._session
    
    @classmethod
    async def check_limit(cls, user_id: int) -> bool:
        """
        Проверка лимита запросов пользователя.
        
        Args:
            user_id (int): ID пользователя
            
        Returns:
            bool: True если лимит не превышен, иначе False
        """
        if cls._user_requests.get(user_id, 0) >= Config.REQUEST_LIMIT:
            return False
        cls._user_requests[user_id] = cls._user_requests.get(user_id, 0) + 1
        return True
    
    @classmethod
    async def get_all_keys(cls) -> Optional[Dict[str, List[Dict[str, Any]]]]:
        """
        Получение всех ключей с сервера Outline.
        
        Returns:
            Optional[Dict]: Словарь с ключами или None в случае ошибки
        """
        try:
            session = await cls.get_session()
            async with session.get("access-keys") as resp:
                if resp.status == 200:
                    return await resp.json()
                logger.error(f"Ошибка API: {resp.status}, тело: {await resp.text()}")
                return None
        except ClientError as e:
            logger.error(f"Ошибка соединения с API: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Непредвиденная ошибка API: {str(e)}")
            return None
    
    @classmethod
    async def create_key(cls, port: int, name: str) -> Optional[Dict[str, Any]]:
        """
        Создание нового ключа.
        
        Args:
            port (int): Номер порта
            name (str): Имя ключа
            
        Returns:
            Optional[Dict]: Информация о созданном ключе или None в случае ошибки
        """
        try:
            session = await cls.get_session()
            async with session.post("access-keys", json={"port": port, "name": name}) as resp:
                if resp.status == 201:
                    return await resp.json()
                logger.error(f"Ошибка создания ключа: {resp.status}, тело: {await resp.text()}")
                return None
        except ClientError as e:
            logger.error(f"Ошибка соединения при создании ключа: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при создании ключа: {str(e)}")
            return None
    
    @classmethod
    async def delete_key(cls, key_id: str) -> bool:
        """
        Удаление ключа по ID.
        
        Args:
            key_id (str): ID ключа для удаления
            
        Returns:
            bool: True если удаление успешно, иначе False
        """
        try:
            session = await cls.get_session()
            async with session.delete(f"access-keys/{key_id}") as resp:
                success = resp.status == 204
                if not success:
                    logger.error(f"Ошибка удаления ключа: {resp.status}, тело: {await resp.text()}")
                return success
        except ClientError as e:
            logger.error(f"Ошибка соединения при удалении ключа: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Непредвиденная ошибка при удалении ключа: {str(e)}")
            return False
    
    @classmethod
    async def close(cls) -> None:
        """Закрывает сессию API при завершении работы."""
        if cls._session and not cls._session.closed:
            await cls._session.close()
            cls._session = None
            logger.info("API сессия закрыта")
    
    @classmethod
    def reset_limits(cls) -> None:
        """Сбрасывает счетчики лимитов запросов."""
        cls._user_requests.clear()
        logger.info("Счетчики лимитов сброшены")