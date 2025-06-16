from telegram.ext import   ApplicationBuilder
from  handlers import start,admin
from dotenv import load_dotenv
import os



         
def main():
    load_dotenv()
    builder = ApplicationBuilder()
    builder.token(os.getenv("TOKEN"))
    app = builder.build()
    app.add_handler(start.get()[0])#CommandHandler start_handler
    app.add_handler(admin.get()[0]) # ConversationHandler login_handler 
    print("Бот запущен")
    return app
     