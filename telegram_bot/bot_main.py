import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_parsing.utils import get_json_from_api, calculate_time
from db_connection import create_engine_connection, Groups, Users
from validators.api_validation import Schedule
from telegram_bot.messages import HELP_MESSAGES, SCHEDULE_MESSAGE
from main import app

load_dotenv()

TELEGRAM_TOKEN = os.getenv('Telegram_token')
API_URL = os.getenv('API_url')

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)

db_engine = create_engine_connection()
session = Session(db_engine)

WEBHOOK_HOST = 'https://deorz-bot.herokuapp.com'
WEBHOOK_PATH = '/message'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 5000

logging.basicConfig(level=logging.INFO)


@dispatcher.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(text=HELP_MESSAGES['start'])


@dispatcher.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(text=HELP_MESSAGES['help'])


@dispatcher.message_handler(commands=['set_group'])
async def command_get_schedule(message: types.Message):
    await message.answer(text=HELP_MESSAGES['set_group'])


@dispatcher.message_handler(commands=['group'])
async def command_group(message: types.Message):
    user = session.scalars(select(Users).filter(
        Users.chat_id == message.chat.id)).first()
    if user is None:
        await message.answer(HELP_MESSAGES['user_not_exist'])
    else:
        group = session.scalars(select(Groups).filter(
            Groups.group_id == user.group_id)).first()
        await message.answer(text=f'Ваша группа {group.group_name}')


@dispatcher.message_handler(commands=['get_schedule'])
async def send_schedule(message: types.Message):
    user = session.scalars(select(Users).filter(
        Users.chat_id == message.chat.id)).first()
    if user is None:
        await message.answer(HELP_MESSAGES['user_not_exist'])
    else:
        time = calculate_time()
        response_json = await get_json_from_api(
            url=API_URL,
            group_id=user.group_id,
            begin_date=time.get('start_time_str'),
            end_date=time.get('end_time_str'))
        if response_json:
            for lesson_object in response_json:
                lesson = Schedule.parse_obj(lesson_object)
                schedule_message = SCHEDULE_MESSAGE.format(
                    day_of_week=lesson.day_of_week,
                    date=lesson.date,
                    group=lesson.group,
                    discipline=lesson.discipline,
                    kind_of_work=lesson.kind_of_work,
                    begin_lesson=lesson.begin_lesson,
                    end_lesson=lesson.end_lesson,
                    lecturer=lesson.lecturer
                )
                await message.answer(text=schedule_message)
        else:
            await message.answer(text='На сегодня пар нет.')


@dispatcher.message_handler()
async def command_set_group(message: types.Message):
    group_name = message.text
    group = session.scalars(select(Groups).filter(
        Groups.group_name == group_name)).first()
    user = session.scalars(select(Users).filter(
        Users.chat_id == message.chat.id)).first()
    if user is None:
        new_user = Users(username=message.chat.username,
                         chat_id=message.chat.id,
                         group_id=group.group_id,
                         )
        session.add(new_user)
        session.commit()
        await message.answer(text='Ваша группа записана')
    else:
        user.group_id = group.group_id
        session.commit()
        await message.answer(text='Ваша группа изменена')


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dispatcher):
    logging.warning('Shutting down..')
    session.close()
    await bot.delete_webhook()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
    start_webhook(
        dispatcher=dispatcher,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
