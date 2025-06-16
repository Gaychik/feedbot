import neurlink
from telegram.ext import   ApplicationBuilder,ContextTypes,MessageHandler, filters,CommandHandler,ConversationHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton
import json

async def start(update:Update, context:ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton('модели')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Добро пожаловать!\nДля работы с моделями нейросетей, нужно выполнить настройку, нажмите на кнопку МОДЕЛИ"
                                    ,reply_markup=reply_markup)


SELECT_MODEL = 1
async def handler_get_models(update:Update, context:ContextTypes.DEFAULT_TYPE):
       await  update.message.reply_text("Укажите номер выбранной модели")
       models = neurlink.get_models()
       message_models = ""
       i=1
       for m in models:
           message_models+=f"{i}.{m}\n"
           i+=1
       await  update.message.reply_text(message_models)
       return SELECT_MODEL
   
async def handler_select_model(update:Update, context:ContextTypes.DEFAULT_TYPE):
        index = int(update.message.text)
        models = neurlink.get_models()
        keyboard =[["Сделать запрос"]]
        await update.message.reply_text(f"Вы упешно выбрали модель - {models[index-1]}",
                                        reply_markup= ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        neurlink.set_model(models[index-1])
        return ConversationHandler.END

async def enter_neurlink_request(update:Update, context:ContextTypes.DEFAULT_TYPE):
     await update.message.reply_text("Введите текст для запроса")
     return "request"
    
async def get_neurlink_request(update:Update, context:ContextTypes.DEFAULT_TYPE):
    request = update.message.text
    try:
        await update.message.reply_text(neurlink.run(request))
    except Exception as e:
          await update.message.reply_text(str(e))
    return ConversationHandler.END


def main():
    builder = ApplicationBuilder()
    builder.token("6429416800:AAGmnFMhkbD8XagsGCgIROmbM2wgwo7ApFE")
    app = builder.build()
    start_cmd_handler = CommandHandler("start",start)
   
    handler_models = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Text("модели"), callback=handler_get_models)],
        states={SELECT_MODEL:[MessageHandler(filters=filters.TEXT, callback=handler_select_model)]}
        ,fallbacks=[])
    
    handler_neurlink_request = ConversationHandler(
        entry_points=[MessageHandler(filters=filters.Text("Сделать запрос"), callback=enter_neurlink_request)],
        states={
                "request":[MessageHandler(filters=filters.TEXT, callback=get_neurlink_request)]
            },
            fallbacks=[])
    app.add_handler(start_cmd_handler)
    app.add_handler(handler_models)
    app.add_handler(handler_neurlink_request)
    print("Бот запущен")
    app.run_polling()

main()