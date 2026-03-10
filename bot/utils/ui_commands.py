from aiogram import Bot
from aiogram.types import BotCommandScopeDefault, BotCommand


async def set_ui_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="◀️ Запуск бота"),
        BotCommand(command="account", description="👤 Аккаунт"),
        BotCommand(command="model", description="⭐️ Выбрать модель"),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
