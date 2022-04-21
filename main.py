import logging
from aiogram import Bot, Dispatcher, executor, types
from aiohttp import web
from config import settings

logging.basicConfig(level=logging.DEBUG)


def main():
    bot = Bot(settings.BOT_TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot)
    app = web.Application()
    app['bot'] = bot
    app.add_routes(webapp_routes)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
