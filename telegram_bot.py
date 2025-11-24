"""
AF IMPERIYA - Telegram Bot
100% To'liq integratsiya
"""

import os
import logging
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
bot = Bot(token=BOT_TOKEN)


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_user_by_chat_id(chat_id):
    """Chat ID bo'yicha user topish"""
    from app import app, User
    with app.app_context():
        return User.query.filter_by(telegram_chat_id=str(chat_id)).first()


def get_user_by_username(username):
    """Telegram username bo'yicha user topish"""
    from app import app, User
    with app.app_context():
        return User.query.filter_by(telegram_username=username).first()


def send_notification(chat_id, message, parse_mode='HTML'):
    """Notification yuborish"""
    try:
        bot.send_message(chat_id=chat_id, text=message, parse_mode=parse_mode)
        return True
    except Exception as e:
        logger.error(f"Notification xatolik: {e}")
        return False


# ============================================
# COMMANDS
# ============================================

def start_command(update: Update, context: CallbackContext):
    """Bot start - avtomatik ulanish"""
    chat_id = update.effective_chat.id
    telegram_username = update.effective_user.username
    first_name = update.effective_user.first_name
    
    from app import app, db, User
    
    with app.app_context():
        # Avval chat_id bo'yicha qidirish
        user = User.query.filter_by(telegram_chat_id=str(chat_id)).first()
        
        if user:
            # Allaqachon ulangan
            keyboard = [
                [InlineKeyboardButton("📋 Mening topshiriqlarim", callback_data='my_tasks')],
                [InlineKeyboardButton("📊 Statistika", callback_data='stats')],
                [InlineKeyboardButton("❓ Yordam", callback_data='help')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            update.message.reply_text(
                f"✅ Xush kelibsiz, {user.full_name}!\n\n"
                f"Siz allaqachon ulanganingiz.\n"
                f"Role: {user.role}\n\n"
                f"Quyidagi tugmalardan foydalaning:",
                reply_markup=reply_markup
            )
            return
        
        # Username bo'yicha qidirish
        if telegram_username:
            user = User.query.filter_by(telegram_username=telegram_username).first()
            
            if user:
                # Avtomatik ulanish
                user.telegram_chat_id = str(chat_id)
                user.telegram_notifications = True
                db.session.commit()
                
                keyboard = [
                    [InlineKeyboardButton("📋 Mening topshiriqlarim", callback_data='my_tasks')],
                    [InlineKeyboardButton("📊 Statistika", callback_data='stats')],
                    [InlineKeyboardButton("❓ Yordam", callback_data='help')]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                update.message.reply_text(
                    f"✅ Muvaffaqiyatli ulandi!\n\n"
                    f"Assalomu alaykum, {user.full_name}!\n"
                    f"Role: {user.role}\n\n"
                    f"Endi sizga topshiriqlar haqida xabarlar kelaveradi.\n\n"
                    f"Quyidagi tugmalardan foydalaning:",
                    reply_markup=reply_markup
                )
                return
        
        # Agar topilmasa
        update.message.reply_text(
            f"👋 Salom, {first_name}!\n\n"
            f"❌ Siz AF IMPERIYA sistemasida ro'yxatdan o'tmagansiz.\n\n"
            f"📝 Ro'yxatdan o'tish:\n"
            f"1. https://af-imperiya.uz ga kiring\n"
            f"2. Registratsiya qiling\n"
            f"3. Telegram username: @{telegram_username or 'username kiriting'}\n"
            f"4. Qayta /start yuboring\n\n"
            f"Yordam: /help"
        )


def help_command(update: Update, context: CallbackContext):
    """Yordam"""
    help_text = """
📚 *AF IMPERIYA Bot - Yordam*

🔹 *Asosiy buyruqlar:*
/start - Botni faollashtirish
/mytasks - Mening topshiriqlarim
/stats - Statistika
/today - Bugungi topshiriqlar
/help - Yordam

🔹 *Funksiyalar:*
✅ Yangi topshiriq haqida xabar
✅ Muddati yaqinlashgan xabar
✅ Chat xabarlari
✅ Izohlar

🔹 *Qo'llab-quvvatlash:*
📧 support@af-imperiya.uz
📱 +998 90 123 45 67
"""
    update.message.reply_text(help_text, parse_mode='Markdown')


def my_tasks_command(update: Update, context: CallbackContext):
    """Mening topshiriqlarim"""
    chat_id = update.effective_chat.id
    user = get_user_by_chat_id(chat_id)
    
    if not user:
        update.message.reply_text("❌ Avval /start buyrug'ini yuboring!")
        return
    
    from app import app, Task
    
    with app.app_context():
        tasks = Task.query.filter_by(
            assigned_to_id=user.id,
            is_active=True
        ).order_by(Task.deadline).all()
        
        if not tasks:
            update.message.reply_text("✅ Sizda topshiriqlar yo'q!")
            return
        
        message = f"📋 *Sizning topshiriqlaringiz ({len(tasks)} ta):*\n\n"
        
        for i, task in enumerate(tasks, 1):
            status_emoji = {
                'pending': '⏳',
                'in_progress': '🔄',
                'completed': '✅'
            }.get(task.status, '❓')
            
            priority_emoji = {
                'high': '🔴',
                'medium': '🟡',
                'low': '🟢'
            }.get(task.priority, '')
            
            message += f"{status_emoji} {priority_emoji} *{i}. {task.title}*\n"
            
            if task.deadline:
                from datetime import datetime
                days_left = (task.deadline - datetime.now()).days
                if days_left < 0:
                    message += f"   ⚠️ Muddat: {abs(days_left)} kun kechikdi\n"
                elif days_left == 0:
                    message += f"   ⏰ Muddat: Bugun!\n"
                else:
                    message += f"   📅 Muddat: {days_left} kun qoldi\n"
            
            message += f"   📊 Progress: {task.progress}%\n\n"
        
        update.message.reply_text(message, parse_mode='Markdown')


def stats_command(update: Update, context: CallbackContext):
    """Statistika"""
    chat_id = update.effective_chat.id
    user = get_user_by_chat_id(chat_id)
    
    if not user:
        update.message.reply_text("❌ Avval /start buyrug'ini yuboring!")
        return
    
    from app import app, Task
    
    with app.app_context():
        tasks = Task.query.filter_by(assigned_to_id=user.id, is_active=True).all()
        
        pending = len([t for t in tasks if t.status == 'pending'])
        in_progress = len([t for t in tasks if t.status == 'in_progress'])
        completed = len([t for t in tasks if t.status == 'completed'])
        
        from datetime import datetime
        overdue = len([t for t in tasks if t.deadline and t.deadline < datetime.now() and t.status != 'completed'])
        
        message = f"""
📊 *Statistika - {user.full_name}*

⏳ Kutilmoqda: {pending}
🔄 Jarayonda: {in_progress}
✅ Bajarilgan: {completed}
⚠️ Kechiktirilgan: {overdue}

📋 Jami: {len(tasks)}
📈 Bajarilish: {int((completed / len(tasks) * 100) if tasks else 0)}%
"""
        
        update.message.reply_text(message, parse_mode='Markdown')


def today_command(update: Update, context: CallbackContext):
    """Bugungi topshiriqlar"""
    chat_id = update.effective_chat.id
    user = get_user_by_chat_id(chat_id)
    
    if not user:
        update.message.reply_text("❌ Avval /start buyrug'ini yuboring!")
        return
    
    from app import app, Task
    from datetime import datetime, date
    
    with app.app_context():
        today = date.today()
        tasks = Task.query.filter(
            Task.assigned_to_id == user.id,
            Task.is_active == True,
            Task.deadline >= datetime.combine(today, datetime.min.time()),
            Task.deadline < datetime.combine(today, datetime.max.time())
        ).all()
        
        if not tasks:
            update.message.reply_text("✅ Bugun uchun topshiriqlar yo'q!")
            return
        
        message = f"📅 *Bugungi topshiriqlar ({len(tasks)} ta):*\n\n"
        
        for i, task in enumerate(tasks, 1):
            status_emoji = {
                'pending': '⏳',
                'in_progress': '🔄',
                'completed': '✅'
            }.get(task.status, '❓')
            
            message += f"{status_emoji} *{i}. {task.title}*\n"
            message += f"   Status: {task.status}\n"
            message += f"   Progress: {task.progress}%\n\n"
        
        update.message.reply_text(message, parse_mode='Markdown')


# ============================================
# CALLBACK HANDLERS
# ============================================

def button_handler(update: Update, context: CallbackContext):
    """Inline button handler"""
    query = update.callback_query
    query.answer()
    
    data = query.data
    
    if data == 'my_tasks':
        my_tasks_command(query, context)
    elif data == 'stats':
        stats_command(query, context)
    elif data == 'help':
        help_command(query, context)


# ============================================
# NOTIFICATION FUNCTIONS
# ============================================

def notify_new_task(user, task):
    """Yangi topshiriq haqida xabar"""
    if not user.telegram_chat_id or not user.telegram_notifications:
        return False
    
    message = f"""
🔔 *Yangi topshiriq!*

📋 *{task.title}*

📝 {task.description or 'Tavsif yo\'q'}

⏰ Muddat: {task.deadline.strftime('%d.%m.%Y %H:%M') if task.deadline else 'Belgilanmagan'}
🎯 Ustunlik: {task.priority}

Topshiriqni ko'rish: https://af-imperiya.uz/tasks/{task.id}
"""
    
    return send_notification(user.telegram_chat_id, message, parse_mode='Markdown')


def notify_task_deadline(user, task, days_left):
    """Muddat yaqinlashgani haqida"""
    if not user.telegram_chat_id or not user.telegram_notifications:
        return False
    
    message = f"""
⚠️ *Muddat yaqinlashdi!*

📋 *{task.title}*

⏰ {days_left} kun qoldi!
Muddat: {task.deadline.strftime('%d.%m.%Y %H:%M')}

Iltimos, o'z vaqtida bajaring!

https://af-imperiya.uz/tasks/{task.id}
"""
    
    return send_notification(user.telegram_chat_id, message, parse_mode='Markdown')


def notify_comment(user, task, comment_user, comment_text):
    """Yangi izoh haqida"""
    if not user.telegram_chat_id or not user.telegram_notifications:
        return False
    
    message = f"""
💬 *Yangi izoh!*

📋 *{task.title}*

👤 {comment_user.full_name}:
"{comment_text}"

https://af-imperiya.uz/tasks/{task.id}
"""
    
    return send_notification(user.telegram_chat_id, message, parse_mode='Markdown')


def notify_chat_message(user, sender, message_text):
    """Chat xabari"""
    if not user.telegram_chat_id or not user.telegram_notifications:
        return False
    
    message = f"""
💬 *Yangi chat xabari!*

👤 {sender.full_name}:
"{message_text}"

Javob berish: https://af-imperiya.uz
"""
    
    return send_notification(user.telegram_chat_id, message, parse_mode='Markdown')


# ============================================
# BOT RUNNER
# ============================================

def run_bot():
    """Bot'ni ishga tushirish"""
    try:
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        # Commands
        dp.add_handler(CommandHandler('start', start_command))
        dp.add_handler(CommandHandler('help', help_command))
        dp.add_handler(CommandHandler('mytasks', my_tasks_command))
        dp.add_handler(CommandHandler('stats', stats_command))
        dp.add_handler(CommandHandler('today', today_command))
        
        # Callbacks
        dp.add_handler(CallbackQueryHandler(button_handler))
        
        # Start bot
        logger.info("🤖 Telegram bot ishga tushdi!")
        print("🤖 Telegram bot ishga tushdi! (@af_imperiya_bot)")
        
        updater.start_polling()
        updater.idle()
        
    except Exception as e:
        logger.error(f"Bot xatolik: {e}")
        print(f"❌ Bot xatolik: {e}")


if __name__ == '__main__':
    run_bot()
