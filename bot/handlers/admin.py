from telegram.ext import(
                    CommandHandler,
                    ContextTypes,
                    ConversationHandler,
                    MessageHandler,
                    filters)

from telegram import Update,ReplyKeyboardMarkup
from utils  import validation
from database import db

async def admin(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите номер телефона 📞 в формате 8(000)(000)(00)(00) ")
    return "phone"

async def get_phone(update:Update,context:ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if validation.validate_phone_number(phone):
        user =  db.get_user_by_phone(phone)
        if user:
            context.user_data["admin"] = user
            keyboard = [
                ["Добавить➕"],
                ["Показать блюда👁‍🗨"]
            ]
            await update.message.reply_text("Добро пожаловать в личный кабинет 👋",
                                            reply_markup=ReplyKeyboardMarkup(keyboard))
            return ConversationHandler.END
        else:
             await update.message.reply_text("Пользователь не найден ❌")
    else:
        await update.message.reply_text("Введенный номер некорректен 🔴")

def get():
    login_handler = ConversationHandler(
        entry_points=[CommandHandler("admin",admin)],
        states={
            "phone": [MessageHandler(filters.TEXT,get_phone)]
        },
        fallbacks=[]
    )
    return [login_handler]
