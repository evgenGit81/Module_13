from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start(message):
    print("Привет! Я бот помогающий твоему здоровью.")

helloshki = ['HWUrban', 'Hi', 'Hello', 'hello', 'hi', 'привет', 'Привет', 'дратути', 'здравствуйте',
             'приветище', 'здравствуй', 'Hi!', 'Hello!', 'hello!', 'hi!', 'привет!', 'Привет!', 'дратути!',
             'Здравствуйте!', 'Приветище!', 'Здравствуй!']

@dp.message_handler(text = helloshki)
async def hello_message(message):
    print("Введите команду /start, чтобы начать общение.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)