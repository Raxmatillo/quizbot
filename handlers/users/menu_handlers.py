from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import db, dp

@dp.message_handler(lambda message: message.text == "🗒 Test tuzish")
async def make_question(message: types.Message, state: FSMContext):
    await message.answer("Test tuzish uchun faylni yuboring")
    await state.set_state('send_file')

@dp.message_handler(state='send_file', content_types='file')
async def get_file(message: types.Message, state: FSMContext):
    file = message.document.file_size