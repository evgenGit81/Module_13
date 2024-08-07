from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

"""Инициализация клавиатуры"""
kb = ReplyKeyboardMarkup(resize_keyboard=True)
bttnclck1 = KeyboardButton(text="Расcчитать")
bttnclck2 = KeyboardButton(text="Информация")
kb.add(bttnclck1, bttnclck2)


kbin = InlineKeyboardMarkup(inline_keyboard=True)
bttn1 = InlineKeyboardButton(text="Рассчитать норму калорий", callback_data="calories")
bttn2 = InlineKeyboardButton(text="Формулы расcчёта", callback_data="formula")
kbin.add(bttn1, bttn2)


calc_menu = kbin

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


helloshki = ['HWUrban', 'Hi', 'Hello', 'hello', 'hi', 'привет', 'Привет', 'дратути', 'здравствуйте',
             'приветище', 'здравствуй', 'Hi!', 'Hello!', 'hello!', 'hi!', 'привет!', 'Привет!', 'дратути!',
             'Здравствуйте!', 'Приветище!', 'Здравствуй!']

@dp.message_handler(text = helloshki)
async def hello_message(message):
    await message.answer("Введите команду /start, чтобы начать общение.")

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup=kb)

@dp.message_handler(text="Информация")
async def show_info(message):
    await message.answer("""Этот бот расчситывает калории 
                            для приведения вас хорошее состояние при средней актвности.""")

"""Подключаем IlineKeyboard"""
@dp.message_handler(text='Расcчитать')
async def main_menu(message):
    await message.answer("Выберите опцию:", reply_markup=calc_menu)

"""Вывод формулы по которой производится рассчет"""
@dp.callback_query_handler(text='formula')
async def get_formulas(callbttn):
    await callbttn.message.answer("для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x 1.55")
    await callbttn.answer()

"""Запрос возраста"""
@dp.callback_query_handler(text='calories')
async def set_age(callbttn):
    await callbttn.message.answer("Укажите свой возраст.")
    await UserState.age.set()
    await callbttn.answer()

"""Запрос роста после получения возраста"""
@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(agetxt=message.text)
    data = await state.get_data()
    await message.answer("Укажите свой рост.")
    await UserState.growth.set()

"""Запрос веса после получения роста"""
@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growthtxt=message.text)
    data = await state.get_data()
    await message.answer("Укажите свой вес.")
    await UserState.weight.set()

"""Рассчет и вывод результата"""
@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weighttxt=message.text)
    data = await state.get_data()
    calories = 10 * float(data['weighttxt']) + 6.25 * float(data['growthtxt']) - 5 * (float(data['agetxt']) + 5) * 1.55
    await message.answer(f"Ваша норма {calories} калорий.")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
