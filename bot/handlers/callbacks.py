from telegram.ext import(
                    CallbackContext,
                    CallbackQueryHandler
                    )
                    

from telegram import Update
from ai import dish_describer
from database import db
from database.models import Dish

async def want_all_know_handler(update:Update,context:CallbackContext):
        query = update.callback_query
        dish_id = int(query.data.split('=')[-1])
        dish = Dish()
        dish.from_tuple(db.get_dish_by_id(dish_id))
        #в первую очередь будет в будущем обращаться к кешу
        processing_msg = await context.bot.send_message(
        chat_id=query.message.chat_id,
        text="Идет обработка 💾..."
        )
        result = db.get_ans_neurlink(dish_id)
        if result == None:
                result = await dish_describer.run(dish)
                db.update_dish_by_id(dish_id,result)
                
        if result:
                await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=processing_msg.message_id,
                text=result
            )
        else: 
                await context.bot.edit_message_text(
                chat_id=query.message.chat_id,
                message_id=processing_msg.message_id,
                text="К нашему сожалению, описание блюда недоступно, обратитесь к официанту😃"
            )
        #нужно обязательно добавить столбец properties, 
        #для характеристик блюда от самого заведения

def get():
    neurlink_handler = CallbackQueryHandler(pattern=r"^dish_id",callback=want_all_know_handler)
    return [neurlink_handler]