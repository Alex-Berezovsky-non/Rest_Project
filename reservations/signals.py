from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings
from .models import Reservation
from .utils.telegram_bot import send_telegram_message

@receiver(post_save, sender=Reservation)
def notify_new_reservation(sender, instance, created, **kwargs):
    if created and instance.id:
        admin_url = reverse('admin:reservations_reservation_change', args=[instance.id])
        full_url = f"{settings.BASE_URL}{admin_url}"
        
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
        
        try:
            send_telegram_message(
                token=settings.TELEGRAM_BOT_TOKEN,
                chat_id=settings.TELEGRAM_CHAT_ID,
                message=message
            )
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления: {e}")