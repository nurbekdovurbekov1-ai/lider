import logging
import threading

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_message(text):
    """Telegram bot orqali xabar yuborish. Token/chat_id sozlanmagan bo'lsa False."""
    token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
    chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
            timeout=10,
        )
        if not resp.ok:
            logger.warning("Telegram xato: %s %s", resp.status_code, resp.text[:300])
            return False
        return True
    except Exception as exc:
        logger.warning("Telegram yuborilmadi: %s", exc)
        return False


def notify_new_order(order):
    """Yangi buyurtma haqida admin ga Telegram xabari (fon rejimida, xatolar buyurtmani buzmaydi)."""
    def _send():
        lines = [
            "🛒 <b>Yangi buyurtma!</b>",
            f"📦 Buyurtma: <b>#{order.order_number}</b>",
            f"👤 Mijoz: {order.user.full_name} ({order.user.phone_number})",
            "",
            "<b>Tarkibi:</b>",
        ]
        for item in order.items.all():
            lines.append(
                f"• {item.product_name} — {item.quantity} dona — {item.total_price:,.0f} so'm"
            )
        addr = order.delivery_address
        if addr:
            address_text = addr.full_address or ", ".join(
                filter(None, [addr.city, addr.street, addr.house_number])
            )
            lines += ["", "<b>Manzil:</b>", address_text]
        if order.notes:
            lines += ["", f"📝 Izoh: {order.notes}"]
        lines += ["", f"💰 Jami: <b>{order.total_amount:,.0f} so'm</b>"]
        send_message("\n".join(lines))

    threading.Thread(target=_send, daemon=True).start()
