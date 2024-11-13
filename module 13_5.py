from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio


token = ''
bot = Bot(token = token)
dp = Dispatcher(bot, storage=MemoryStorage())
kp = ReplyKeyboardMarkup()
button = KeyboardButton(text = 'Расcчитать')
button1 = KeyboardButton(text = 'Информация')

kp.add(button)
kp.add(button1)
greet_kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(button)



@dp.message_handler(commands = ['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью!', reply_markup = kp)

class UserState (StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Расcчитать')
async def  set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def  send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = (10 * weight) + (6.25 * growth) - (5 * age) + 5
    await message.answer(f"Ваша норма калорий: {calories}")
    await state.finish()

# @dp.message_handler(text='Информация')
# async def show_info(message: types.Message, state: FSMContext):
#     data = await state.get_data()  # Получаем данные из состояния
#     if not data:
#         await message.answer("Информация о калориях недоступна. Пожалуйста, воспользуйтесь кнопкой 'Расcчитать' для ввода данных.")
#         return
#
#     try:
#         age = data.get('age')
#         growth = data.get('growth')
#         weight = data.get('weight')
#
#         await message.answer(f"Последние введенные данные:\nВозраст: {age}\nРост: {growth}\nВес: {weight}")
#     except KeyError:
#         await message.answer("Данные не найдены. Пожалуйста, воспользуйтесь кнопкой 'Расcчитать' для ввода данных.")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)