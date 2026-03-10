import asyncio
from aiogram.enums import ParseMode
from aiogram.types import Message

MAX_LENGTH = 4096


async def send_answer_parts(message: Message, text: str):
    if len(text) <= MAX_LENGTH:
        await message.answer(text, parse_mode=ParseMode.MARKDOWN)
        return

    parts = [text[i : i + MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]
    await asyncio.gather(*(message.answer(part) for part in parts))
