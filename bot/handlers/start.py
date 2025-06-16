from telegram.ext import CommandHandler,ContextTypes
from telegram import Update 

async def start(update:Update, context: ContextTypes.DEFAULT_TYPE):
   await update.message.reply_text("""
👋 Добро пожаловать в ресторан FitFood! 
 Я помогу вам выбрать идеальное блюдо, рассчитать калории и оформить заказ 🍽️""")

def get():
    return [CommandHandler("start",start)]


    


