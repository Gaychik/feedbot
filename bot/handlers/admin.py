from telegram.ext import(
                    CommandHandler,
                    ContextTypes,
                    ConversationHandler,
                    MessageHandler,
                    filters)
                    

from telegram import Update,ReplyKeyboardMarkup,InlineKeyboardMarkup,InlineKeyboardButton
from utils  import validation
from database import db
from database import models

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
    add_dish_handler = ConversationHandler(
         entry_points=[MessageHandler(filter.Text("Добавить➕"),start_add_dish)],
         states={
              "name": [MessageHandler(filters.TEXT,get_name)],
              "desc": [MessageHandler(filters.TEXT,get_desc)],
              "photo":[MessageHandler(filters.TEXT,get_photo)]
         },
         fallbacks=[]
    )
    show_handler = MessageHandler(filters.Text("Показать блюда👁‍🗨",show))
    return [login_handler,add_dish_handler,show_handler]


async def show(update:Update,context:ContextTypes.DEFAULT_TYPE):
    dishes:list[models.Dish] = db.get_dishes()
    if len(dishes)==0: 
         await update.message.reply_text("Блюда отсутствуют...")
    else:   
        for d in dishes: 
            text = (
                        f"Название:{d.name}\n"
                        f"Цена 💵: {d.price}\n"
                        f"Теги: {d.tags}\n"
                        f"Описание:\n{d.desc}"
                    )
            keyboard = [
                [InlineKeyboardButton(text = "Хочу все знать",callback_data = f"{d.id}")]
            ]
            await update.message.reply_photo(d.photo,text,reply_markup=InlineKeyboardMarkup(keyboard))


async def start_add_dish(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Введите название блюда")
    return "name"

async def get_name(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
   
    await update.message.reply_text("Сделайте описание в формате: "
                                    "[Цена]"
                                    "[Теги: Веган/Мясоед/Безглютен/Диабетик]"
                                    "[Описание]")
    return "desc"

async def get_desc(update:Update,context:ContextTypes.DEFAULT_TYPE):
       context.user_data["desc"] = update.message.text
       await update.message.reply_text("Отправь фото")
       return "photo"


async def get_photo(update:Update,context:ContextTypes.DEFAULT_TYPE):
       photo = await update.message.photo[-1].get_file()
       binary_photo = await  photo.download_as_bytearray()
       context.user_data["photo"] = binary_photo
       result = save_dish(context.user_data)
       if result: 
            await update.message.reply_text("Блюдо добавлено ✅")
       else:
             await update.message.reply_text("Ошибка при добавлении ☹️")
       return ConversationHandler.END

def save_dish(data):
     name = data["name"]
     photo = data["photo"]
     price,tags,desc = data["desc"].split('\n')
     dish = models.Dish(name,int(price),tags,desc,photo)
     return db.add_dish(dish)
          
     
 
     
    
    