import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_parsing.utils import get_json_from_api, calculate_time
from db_connection import create_engine_connection, Groups, Users
from validators.api_validation import Schedule
from telegram_bot.messages import HELP_MESSAGES, SCHEDULE_MESSAGE

load_dotenv()

TELEGRAM_TOKEN = os.getenv('Telegram_token')
API_URL = os.getenv('API_url')

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)

db_engine = create_engine_connection()
session = Session(db_engine)


@dispatcher.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(text=HELP_MESSAGES['start'])


@dispatcher.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(text=HELP_MESSAGES['help'])


@dispatcher.message_handler(commands=['set_group'])
async def command_get_schedule(message: types.Message):
    await message.answer(text=HELP_MESSAGES['set_group'])


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
        for lesson_object in response_json:
            lesson = Schedule.parse_obj(lesson_object)
            if lesson.day_of_week == time.get('day_now').capitalize():
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
                break


@dispatcher.message_handler()
async def command_set_group(message: types.Message):
    group_name = message.text
    group_query = select(Groups).where(Groups.group_name == group_name)
    group = session.scalars(group_query).one()
    user = session.scalars(select(Users).filter(
        Users.id == message.chat.id)).first()
    if user is None:
        user = Users(username=message.chat.username,
                     chat_id=message.chat.id,
                     group_id=group.group_id,
                     )
        session.add(user)
        session.commit()
        await message.answer(text='Ваша группа записана')


executor.start_polling(dispatcher, skip_updates=True)
