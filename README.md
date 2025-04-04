![image](https://github.com/user-attachments/assets/1d60abaa-b917-49d4-ab9c-2c4341fde3b2)# PandaVPN Telegram Bot

Телеграм-бот для управления VPN-сервером на базе Outline VPN API. Позволяет создавать, просматривать и удалять ключи доступа, а также обрабатывать запросы от обычных пользователей.

## Возможности

### Для администратора:
- Создание новых ключей доступа с указанием порта и имени
- Просмотр списка всех ключей
- Просмотр детальной информации о ключе
- Удаление ключей
- Получение уведомлений о запросах на создание ключей от пользователей

### Для обычных пользователей:
- Запрос на получение VPN-ключа через администратора
- Удобный интерфейс с inline-клавиатурами

## Технические особенности
- Асинхронная работа с API Outline
- Управление состояниями через FSM (Finite State Machine)
- Система ограничения количества запросов от пользователей
- Логирование всех действий и ошибок
- Проверка подключения к интернету при запуске

## Требования
- Python 3.13.1
- aiogram 3.19.0
- aiohttp 3.11.14
- python-dotenv 1.0.0+

## Установка и настройка

1. Клонировать репозиторий:
```bash
git clone https://github.com/yourusername/PandaVPN_Bot.git
cd PandaVPN_Bot
```

2. Установить зависимости:
```bash
pip install -r requirements.txt
```

3. Создать файл `.env` в корневой директории проекта со следующими параметрами:
```
TELEGRAM_TOKEN=your_telegram_bot_token
OUTLINE_API_URL=your_outline_server_api_url
OUTLINE_API_TOKEN=your_outline_api_token
ADMIN_ID=your_telegram_id
REQUEST_LIMIT=3
```

4. Запустить бота:
```bash
python -m PandaVPNAR.bot
```

## Структура проекта

```
PandaVPNAR/
│
├── api/
│   ├── __init__.py
│   └── outline.py          # API клиент для Outline
│
├── handlers/
│   ├── __init__.py
│   ├── admin.py            # Обработчики для администратора
│   └── user.py             # Обработчики для обычных пользователей
│
├── keyboards/
│   ├── __init__.py
│   └── inline.py           # Инлайн-клавиатуры
│
├── states/
│   ├── __init__.py
│   └── forms.py            # Классы состояний
│
├── utils/
│   ├── __init__.py
│   └── decorators.py       # Полезные декораторы
│
├── bot.py                  # Основной файл для запуска бота
├── config.py               # Конфигурация и константы
└── requirements.txt        # Зависимости проекта
```

## Лицензия
MIT

## Автор
TG: @Toksi69
