"""
AF IMPERIYA - Telegram Bot Integration
Real-time push notifications va bot funksiyalari
"""

import os
import asyncio
from telegram import Bot
from telegram.error import TelegramError


class TelegramBot:
    """Telegram bot sinfi"""
    
    def __init__(self, token):
        self.token = token
        self.bot = Bot(token=token) if token else None
    
    async def send_message_async(self, chat_id, message):
        """Asinxron xabar yuborish"""
        if not self.bot:
            return False
        
        try:
            await self.bot.send_message(chat_id=chat_id, text=message)
            return True
        except TelegramError as e:
            print(f"Telegram xatolik: {e}")
            return False
    
    def send_message(self, chat_id, message):
        """Sinxron xabar yuborish"""
        if not self.bot:
            return False
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                self.send_message_async(chat_id, message)
            )
            loop.close()
            return result
        except Exception as e:
            print(f"Xabar yuborishda xatolik: {e}")
            return False
    
    def send_task_notification(self, task, user, notification_type):
        """Topshiriq bo'yicha xabarnoma"""
        if not user.telegram_id:
            return False
        
        messages = {
            'new_task': f"🆕 Yangi topshiriq!\\n\\n📋 {task.title}\\n⏰ Muddat: {task.due_date.strftime('%d.%m.%Y') if task.due_date else 'Belgilanmagan'}",
            'task_approved': f"✅ Topshiriq tasdiqlandi!\\n\\n📋 {task.title}",
            'task_rejected': f"❌ Topshiriq rad etildi!\\n\\n📋 {task.title}",
            'task_overdue': f"⚠️ Topshiriq muddati o'tdi!\\n\\n📋 {task.title}",
            'task_reminder': f"⏰ Eslatma: Topshiriq muddati yaqinlashmoqda!\\n\\n📋 {task.title}"
        }
        
        message = messages.get(notification_type, "Yangi xabarnoma")
        return self.send_message(user.telegram_id, message)


# Global bot instance
telegram_bot = None

def init_telegram_bot(token):
    """Bot ni boshlash"""
    global telegram_bot
    if token:
        telegram_bot = TelegramBot(token)
        return telegram_bot
    return None

def get_telegram_bot():
    """Bot instanceni olish"""
    return telegram_bot
