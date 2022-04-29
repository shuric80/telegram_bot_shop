from aiogram import Dispatcher, types, Bot
from aiogram.utils.executor import set_webhook
from aiohttp import web
from config import settings
from web_app import routes as webapp_routes


async def on_startup(dp: Dispatcher):
    await dp.bot.set_webhook(settings.WEBHOOK.URL)


async def on_shutdown(dp: Dispatcher):
    await dp.bot.delete_webhook()


async def cmd_start(message: types.Message):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='Order Food',
                                   web_app=types.WebAppInfo(
                                       url=f'https://{settings.WEBHOST.HOST}'))
    ]])
    await message.answer('<b>Hey!</b>You can order', reply_markup=markup)


async def ordered(message: types.Message):
    await message.reply('<b> Thank you for your order!')


def main():
    bot = Bot(settings.BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher(bot)
    app = web.Application()
    app["bot"] = bot
    app.add_routes(webapp_routes)
    app.router.add_static(prefix='/static', path='static')
    set_webhook(
        dispatcher=dp,
        webhook_path=settings.WEBHOOK.PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        web_app=app,
    )
    dp.register_message_handler(cmd_start, commands=["start"])
    dp.register_message_handler(ordered, lambda message: message.via_bot)
    web.run_app(app, port=settings.WEBAPP.PORT, host=settings.WEBAPP.HOST)


if __name__ == "__main__":
    main()
