from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("""Привет! Я бот помогающий твоему здоровью. 
                         Для подсчета количества колорий отправьте сообщение 'Calories'"""
                         )

helloshki = ['HWUrban', 'Hi', 'Hello', 'hello', 'hi', 'привет', 'Привет', 'дратути', 'здравствуйте',
             'приветище', 'здравствуй', 'Hi!', 'Hello!', 'hello!', 'hi!', 'привет!', 'Привет!', 'дратути!',
             'Здравствуйте!', 'Приветище!', 'Здравствуй!']

@dp.message_handler(text = helloshki)
async def hello_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

"""Запрос возраста и сохранение его"""
@dp.message_handler(text='Calories')
async def set_age(message):
    await message.answer("Укажите свой возраст.")
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(agetxt=message.text)
    data = await state.get_data()
    await message.answer("Укажите свой рост.")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growthtxt=message.text)
    data = await state.get_data()
    await message.answer("Укажите свой вес.")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weighttxt=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weighttxt']) + 6.25 * float(data['growthtxt']) - 5 * (float(data['agetxt']) + 5) * 1.55
    await message.answer(f"Ваша норма {calories} калорий.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
