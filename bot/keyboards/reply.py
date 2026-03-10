from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Аккаунт", style="primary")],
        [KeyboardButton(text="Модель", style="primary")],
    ],
    resize_keyboard=True,
)
