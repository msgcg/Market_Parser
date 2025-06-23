from telegram import Bot
from telegram.request import HTTPXRequest
import httpx
import asyncio
# Токен бота (замени на свой)
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_ID"  # Групповой или личный ID


# Передаем настроенный HTTPX клиент в бот
request = HTTPXRequest(pool_timeout=2.0,connection_pool_size=10)
bot = Bot(token=TOKEN, request=request)


async def send_message_totg(text: str):
    """Асинхронная функция отправки сообщения в Telegram-чат."""
    try:
        await bot.send_message(chat_id=CHAT_ID, text=text)
    except Exception as e:
        if "Event loop is closed" in str(e):
            pass  # Игнорируем ошибку
        else:
            print(f"Ошибка отправки сообщения: {e}")  # Логируем остальные ошибки

# Функция для синхронного вызова
def send_debug(text):
    asyncio.run(send_message_totg(str(text)))
