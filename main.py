import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Хранение состояния бота (включен/выключен) для каждого пользователя
active_users = set()

# Кнопки меню
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(KeyboardButton("Старт"), KeyboardButton("Выключить"))
keyboard.add(KeyboardButton("Инфобез"))

@dp.message(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer("Бот запущен! Используйте кнопки для управления.", reply_markup=keyboard)

@dp.message(lambda message: message.text == "Старт")
async def start_bot(message: types.Message):
    user_id = message.from_user.id
    active_users.add(user_id)
    await message.answer("Бот включен! Теперь вы будете получать уведомления.")

@dp.message(lambda message: message.text == "Выключить")
async def stop_bot(message: types.Message):
    user_id = message.from_user.id
    active_users.discard(user_id)
    await message.answer("Бот выключен! Уведомления отключены.")

@dp.message(lambda message: message.text == "Инфобез")
async def infosec_timer(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_users:
        await message.answer("Таймер на 5 минут запущен!")
        await asyncio.sleep(300)  # 5 минут
        await message.answer("Прошло 5 минут! Таймер на 15 минут запущен!")
        await asyncio.sleep(900)  # 15 минут
        await message.answer("Прошло 15 минут!")

async def send_black_night():
    now = datetime.now()
    if now.weekday() == 5 and now.hour == 21:  # Суббота 21:00
        for user_id in active_users:
            try:
                await bot.send_message(user_id, "Приближается Черная ночь")
            except Exception as e:
                logging.error(f"Ошибка отправки сообщения: {e}")

async def send_va_sec():
    now = datetime.now()
    if now.minute == 29 and now.hour % 2 == 1:  # 01:29, 03:29, ... 23:29
        for user_id in active_users:
            try:
                await bot.send_message(user_id, "Отчет va_sec")
            except Exception as e:
                logging.error(f"Ошибка отправки сообщения: {e}")

# Добавляем задачи в планировщик
scheduler.add_job(send_black_night, "cron", day_of_week="sat", hour=21, minute=0)
scheduler.add_job(send_va_sec, "cron", minute=29)

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
