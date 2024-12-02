import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ParseMode

from states.Register import RegisterState
from utils.shortcuts import safe_markdown
from data.config import ADMINS
from keyboards.inline.buttons import register_markup
from keyboards.default.buttons import contact_markup, menu_keyboards

from loader import dp, bot, db


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    await message.answer(f"Assalom alaykum <b>{message.from_user.full_name}</b>\nBotdan foydalanish uchun ro'yxatdan o'tishingiz kerak!", reply_markup=register_markup)


@dp.callback_query_handler(text_contains="register")
async def start_reg_state(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=None)

    await call.message.answer("To'liq ism familyangizni yozing")
    await RegisterState.full_name.set()

@dp.message_handler(state=RegisterState.full_name, content_types='text')
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer("Iltimos, telefon raqamingizni yuboring", reply_markup=contact_markup)
    await RegisterState.phone.set()


@dp.message_handler(state=RegisterState.phone, content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number
    print(phone)
    data = await state.get_data()
    full_name = data.get('full_name')
    telegram_id = message.from_user.id
    user = None
    try:
        user = db.add_user(full_name=full_name, phone=phone, telegram_id=telegram_id)
    except Exception as error:
        logging.info(error)
    if user:
        count = await db.count_users()
        msg = (f"[{safe_markdown(user['full_name'])}](tg://user?id={user['telegram_id']}) bazaga qo'shildi\.\nBazada {count} ta foydalanuvchi bor\.")
    else:
        msg = f"[{safe_markdown(full_name)}](tg://user?id={telegram_id}) bazaga oldin qo'shilgan"
    for admin in ADMINS:
        try:
            await bot.send_message(
                chat_id=admin,
                text=msg,
                parse_mode=ParseMode.MARKDOWN_V2
            )
        except Exception as error:
            logging.info(f"Data did not send to admin: {admin}. Error: {error}")
    await state.finish()
    await message.answer(f"Assalomu alaykum {safe_markdown(full_name)}\!", parse_mode=ParseMode.MARKDOWN_V2, reply_markup=menu_keyboards)