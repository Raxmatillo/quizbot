import logging
from aiogram import executor

from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands




async def database_connected():
    # Ma'lumotlar bazasini yaratamiz:
    # await db.drop_users()
    # db.delete_users()
    db.create_table_users()
    db.create_table_quizzes()
    db.create_table_tests()


async def on_startup(dispatcher):  

    logging.info("Database connected")
    await database_connected()

    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
