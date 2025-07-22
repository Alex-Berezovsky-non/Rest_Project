import logging
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from .models import Reservation 

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False
    logger.error("Библиотека 'requests' не установлена. Установите её командой: pip install requests")

@receiver(post_save, sender=Reservation)
def notify_new_reservation(sender, instance: Reservation, created: bool, **kwargs):
    """
    Отправляет уведомление в Telegram о новом бронировании
    """
    if not created or not instance.id:
        return

    if not REQUESTS_AVAILABLE:
        logger.error("Невозможно отправить уведомление: библиотека 'requests' недоступна")
        return

    try:
        telegram_token = getattr(settings, 'TELEGRAM_BOT_API_KEY', None)
        chat_id = getattr(settings, 'TELEGRAM_USER_ID', None)
        
        if not telegram_token or not chat_id:
            logger.error("Telegram настройки не найдены в settings.py!")
            return

        base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
        admin_url = reverse('admin:reservations_reservation_change', args=[instance.id])
        full_url = f"{base_url}{admin_url}"

        message = (
            "📅 *Новое бронирование!*\n"
            f"🔖 *ID:* {instance.id}\n"
            f"🍽 *Столик №:* {instance.table.number}\n"
            f"👥 *Гостей:* {instance.guests}\n"
            f"👤 *Имя:* {instance.customer_name}\n"
            f"📞 *Телефон:* `{instance.customer_phone}`\n"
            f"✉️ *Email:* {instance.customer_email}\n"
            f"⏰ *Дата/время:* {instance.date.strftime('%d.%m.%Y')} {instance.time.strftime('%H:%M')}\n"
            f"⏳ *Длительность:* {instance.duration} ч.\n"
            f"📝 *Пожелания:* {instance.special_requests or 'нет'}\n"
            f"🔗 [Ссылка в админку]({full_url})"
        )

        response = requests.post(
            f"https://api.telegram.org/bot{telegram_token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": True
            },
            timeout=10
        )

        if response.status_code == 200:
            logger.info(f"Уведомление о бронировании #{instance.id} отправлено в Telegram")
        else:
            logger.error(f"Ошибка Telegram API: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка соединения: {str(e)}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {str(e)}", exc_info=True)