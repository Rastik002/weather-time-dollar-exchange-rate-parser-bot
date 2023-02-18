from aiogram.types import ReplyKeyboardMarkup

menuUser = ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
menuUser.add("Парсинг погоды","Парсинг курса доллара", "Парсинг времени")