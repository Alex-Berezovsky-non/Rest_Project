import logging
from typing import Optional
from telegram import Bot
from asgiref.sync import async_to_sync
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

async def async_send_telegram_message(
    token: str,
    chat_id: int,
    message: str,
    parse_mode: Optional[str] = "Markdown"
) -> None:
    try:
        bot = Bot(token=token) 
        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode=parse_mode,
            disable_web_page_preview=True
        )
        logger.info(f'Сообщение отправлено в чат {chat_id}')
    except Exception as e:
        logger.error(f"Ошибка отправки в Telegram: {e}")
        raise

def send_telegram_message(token: str, chat_id: int, message: str) -> None:
    async_to_sync(async_send_telegram_message)(token, chat_id, message)