import logging
from aiogram import Bot, Dispatcher

from bot.utils import set_ui_commands, config, setup_logging
from bot.handlers import routers
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

setup_logging(filename="bot.log")
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(
        config.webhook_url, secret_token=config.webhook_secret.get_secret_value()
    )
    await set_ui_commands(bot)


def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(*routers)
    dp.startup.register(on_startup)

    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=config.webhook_secret.get_secret_value(),
    )
    webhook_requests_handler.register(app, path=config.webhook_path.get_secret_value())
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="0.0.0.0", port=8000)


try:
    main()
except KeyboardInterrupt, SystemExit:
    logger.warning("Bot stopped manually")
