from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

contact_markup = ReplyKeyboardMarkup(
    [
        [KeyboardButton(text="Telefon raqamni yuborish 📞", request_contact=True)]
    ], resize_keyboard=True
)


menu_keyboards = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="🗒 Test tuzish"),
            KeyboardButton(text="📚 Mening testlarim")
        ],
        [
            KeyboardButton(text="⭐️ Kredit olish")
        ]
    ], resize_keyboard=True
)