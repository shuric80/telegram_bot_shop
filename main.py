import logging
from aiogram import Bot, Dispatcher, executor, types
from config import settings

logging.basicConfig(level=logging.DEBUG)

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_wellcome(message: types.Message):
    await message.reply("Hi!")


@dp.message_handler()
async def send_echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
