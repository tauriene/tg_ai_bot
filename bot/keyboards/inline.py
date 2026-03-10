from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.db import get_ai_models


async def get_ai_models_kb(user_ai_model: str) -> InlineKeyboardMarkup | None:
    ai_models = await get_ai_models()
    if not ai_models:
        return None

    kb = InlineKeyboardBuilder()
    for model in ai_models:
        kb.add(
            InlineKeyboardButton(
                text=(
                    f"✅ {model.name}" if user_ai_model == model.name else model.name
                ),
                callback_data=f"model_{model.id}_{model.name}",
            )
        )

    return kb.adjust(1).as_markup()
