from telegram.ext import   ApplicationBuilder
from bot.handlers.dialogs import change_dish
from  handlers import start,admin,callbacks,menu
from dotenv import load_dotenv
import os




         
def main():
    load_dotenv()
    builder = ApplicationBuilder()
    builder.token(os.getenv("TOKEN"))
    app = builder.build()
    app.add_handler(start.get()[0])#CommandHandler start_handler
    app.add_handler(admin.get()[0]) # ConversationHandler login_handler 
    app.add_handler(admin.get()[1])# ConversationHandler add_dish_handler
    app.add_handler(menu.get()[0])# MessageHandler show_handler
    app.add_handler(callbacks.get()[0])# CallBackQueryHandler handler_neurlink
    app.add_handler(callbacks.get()[1])# CallBackQueryHandler show_props_handler
    app.add_handler(callbacks.get()[2])# CallBackQueryHandler add_to_card_handler
    app.add_handler(change_dish.get()[0])# ConversationHandler handler
 
    print("Бот запущен")
    return app
     