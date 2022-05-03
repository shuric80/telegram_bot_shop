import asyncio

import jinja2
from aiogram import Dispatcher, types, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils import executor
from aiogram.utils.executor import set_webhook
from aiohttp import web
from aiohttp.web_request import Request

from config import settings
from web_app import routes as webapp_routes
import aiohttp_jinja2

bot = Bot(token=settings.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


async def web_start(request: Request):
    return await aiohttp_jinja2.render_template_async('index.html')


app = web.Application()
app.add_routes([web.get('/web-start', web_start)])
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader('web'),
                     enable_async=True)


async def on_startup(dps: Dispatcher):
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host='0.0.0.0', port=45678))


async def on_shutdown(dps: Dispatcher):
    await dps.storage.close()
    await dps.storage.wait_closed()


@dp.message_handler(CommandStart())
@dp.throttled(rate=2)
async def cmd_start(message: types.Message):
    keybord = types.InlineKeyboardMarkup(inline_keyboard=[[
        types.InlineKeyboardButton(text='Order Food',
                                   web_app=types.WebAppInfo(
                                       url=f'https://{settings.WEBHOST.HOST}'))
    ]])
    await message.reply('<b>Hey!</b>You can order', reply_markup=keybord)


def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == '__main__':
    main()
