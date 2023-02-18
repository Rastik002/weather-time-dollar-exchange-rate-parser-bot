from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from keyboards import *

storage = MemoryStorage()
bot = Bot('') # BOT TOKEN
dp = Dispatcher(bot, storage=storage)

option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)

class UserState(StatesGroup):
    pars_time = State()
    pars_weather = State()
    pars_dollars = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer('ку бро.', reply_markup=menuUser)

@dp.message_handler(content_types=['text'])
async def handler(message: types.Message):
    if message.text == 'Парсинг курса доллара':
        await message.answer('Введите цифры в долларах:')
        await UserState.pars_dollars.set()

    elif message.text == 'Парсинг времени':
        await message.answer('Введите название города:')
        await UserState.pars_time.set()

    elif message.text == 'Парсинг погоды':
        await message.answer('Введите название города:')
        await UserState.pars_weather.set()

@dp.message_handler(state=UserState.pars_time)
async def time(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            await message.answer('Введите правильное название!', reply_markup=menuUser)
            await state.reset_state(with_data=False)
        else:
            sity = message.text
            driver.get(f'https://yandex.ru/search/?text=время+в+{sity}&lr=237&clid=2456107')
            time = driver.find_element(By.CLASS_NAME, 'link_theme_black').text
            await message.answer(f'Время в городе {sity}: <code>{time}</code>', parse_mode='html')
            await state.reset_state(with_data=False)
    except:
        await message.answer('что-то пошло не так', reply_markup=menuUser)
        await state.reset_state(with_data=False)

@dp.message_handler(state=UserState.pars_weather)
async def weather(message: types.Message, state: FSMContext):
    try:
        if message.text.isdigit():
            await message.answer('Введите правильное название!')
            await state.reset_state(with_data=False)
        else:
            sity = message.text
            driver.get(f'https://yandex.ru/search/?clid=2456107&text=погода++в+{sity}&l10n=ru&lr=237')
            weather = driver.find_element(By.CLASS_NAME, 'weather-forecast__current-temp').text
            await message.answer(f'Сейчас в городе {sity} <code>{weather}</code>', parse_mode='html')
            await state.reset_state(with_data=False)
    except:
        await message.answer('что-то пошло не так', reply_markup=menuUser)
        await state.reset_state(with_data=False)

@dp.message_handler(state=UserState.pars_dollars)
async def dollars(message: types.Message, state: FSMContext):
    if message.text.isdigit():
        summ = message.text
        driver.get('https://finance.rambler.ru/currencies/USD/')
        input_tab = driver.find_element(By.CLASS_NAME, 'finance-input')
        input_tab.send_keys(f'{summ}')
        enter_tab = driver.find_element(By.CLASS_NAME, 'rui-Button-block')
        enter_tab.click()
        result = driver.find_element(By.XPATH, '/html/body/div[8]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[1]/div[4]').text
        await message.answer(f'<code>{summ}$ в рублях: {result} RUB</code>', parse_mode='html')
        await state.reset_state(with_data=False)
    else:
        await message.answer('Введите число.', reply_markup=menuUser)
        await state.reset_state(with_data=False)

if __name__ == '__main__':
	executor.start_polling(dispatcher=dp, skip_updates=True)
