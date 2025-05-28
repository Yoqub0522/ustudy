import logging
import requests
from html import escape

class TelegramHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        # HTML xavfsizligi uchun matnni escape qilamiz
        log_entry = escape(self.format(record))

        # Qo‘shimcha: chiroyli formatlash
        formatted_message = (
            f"<b>Log darajasi:</b> {record.levelname}\n"
            f"<b>Modul:</b> {record.name}\n"
            f"<b>Xabar:</b> <code>{log_entry}</code>"
        )

        url = f'https://api.telegram.org/bot{self.token}/sendMessage'
        payload = {
            'chat_id': self.chat_id,
            'text': formatted_message,
            'parse_mode': 'HTML'
        }

        try:
            requests.post(url, data=payload, timeout=5)
        except Exception as e:
            print("Telegram log error:", e)
