from telegram.ext import(
                    CallbackContext
                    )
                    

from telegram import Update
from ai import dish_describer
from database import db
async def want_all_know_handler(update:Update,context:CallbackContext):
        query = update.callback_query
        dish_id = int(query.data)
        dish =  db.get_dish_by_id(dish_id)
        #в первую очередь будет в будущем обращаться к кешу
        result = dish_describer.run(dish)
        db.update_dish_by_id(dish_id,result)
        await update.message.reply_text(result)
        #нужно обязательно добавить столбец properties, 
        #для характеристик блюда от самого заведения