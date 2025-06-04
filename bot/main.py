from telegram.ext import   ApplicationBuilder
from  handlers import start
from dotenv import load_dotenv
import os



         
def main():
    load_dotenv()
    builder = ApplicationBuilder()
    builder.token(os.getenv("TOKEN"))
    app = builder.build()
    app.add_handler(start.get())
    
    print("Бот запущен")
    return app
     