from aiogram import Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_webhook
from sqlalchemy import select
from sqlalchemy.orm import Session

from api_parsing.utils import (calculate_time, get_json_from_api,
                               get_schedule_message)
from db_connection import Groups, Users, create_engine_connection
from telegram_bot.keyboard import schedule_keyboard
from telegram_bot.messages import (HELP_MESSAGES, LOGGER_MESSAGES)
from telegram_bot.settings import (API_URL, TELEGRAM_TOKEN, WEBAPP_HOST,
                                   WEBAPP_PORT, WEBHOOK_PATH,
                                   WEBHOOK_URL, logger)

bot = Bot(token=TELEGRAM_TOKEN)
dispatcher = Dispatcher(bot)
dispatcher.middleware.setup(LoggingMiddleware())

db_engine = create_engine_connection()
session = Session(db_engine)


@dispatcher.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.answer(text=HELP_MESSAGES['start'],
                         reply_markup=schedule_keyboard)


@dispatcher.message_handler(commands=['help'])
async def command_help(message: types.Message):
    await message.answer(text=HELP_MESSAGES['help'],
                         reply_markup=schedule_keyboard)


@dispatcher.message_handler(commands=['set_group'])
async def command_get_schedule(message: types.Message):
    await message.answer(text=HELP_MESSAGES['set_group'],
                         reply_markup=schedule_keyboard)


@dispatcher.message_handler(commands=['group'])
async def command_group(message: types.Message):
    user = session.scalars(select(Users).filter(
        Users.chat_id == message.chat.id)).first()
    if user is None:
        await message.answer(HELP_MESSAGES['user_not_exist'],
                             reply_markup=schedule_keyboard)
    else:
        group = session.scalars(select(Groups).filter(
            Groups.group_id == user.group_id)).first()
        await message.answer(text=f'Ваша группа {group.group_name}',
                             reply_markup=schedule_keyboard)


@dispatcher.message_handler(commands=['get_schedule'])
async def send_schedule(message: types.Message):
    user = session.scalars(select(Users).filter(
        Users.chat_id == message.chat.id)).first()
    if user is None:
        await message.answer(HELP_MESSAGES['user_not_exist'],
                             reply_markup=schedule_keyboard)
    else:
        time = calculate_time()
        response_json = await get_json_from_api(
            url=API_URL,
            group_id=user.group_id,
            begin_date=time.get('start_time_str'),
            end_date=time.get('end_time_str'))
        if response_json:
            schedule_message = await get_schedule_message(response_json)
            await message.answer(text=schedule_message,
                                 reply_markup=schedule_keyboard)
        else:
            await message.answer(text='На сегодня пар нет.',
                                 reply_markup=schedule_keyboard)


@dispatcher.message_handler(
    regexp=r"^[А-Я|а-я]*-\d{2,3}[А-Я|а-я]?-\d{2}")
async def command_set_group(message: types.Message):
    group_name = message.text
    group = session.scalars(select(Groups).filter(
        Groups.group_name == group_name)).first()
    if group is None:
        logger.error(LOGGER_MESSAGES['invalid_group'])
        await message.answer(text=LOGGER_MESSAGES['invalid_group'],
                             reply_markup=schedule_keyboard)
    else:
        user = session.scalars(select(Users).filter(
            Users.chat_id == message.chat.id)).first()
        if user is None:
            new_user = Users(chat_id=message.chat.id,
                             group_id=group.group_id,
                             )
            session.add(new_user)
            session.commit()
            await message.answer(text='Ваша группа записана',
                                 reply_markup=schedule_keyboard)
        else:
            user.group_id = group.group_id
            session.commit()
            await message.answer(text='Ваша группа изменена',
                                 reply_markup=schedule_keyboard)


@dispatcher.message_handler()
async def cant_talk(message: types.Message):
    if message.text.startswith('/'):
        await message.answer(HELP_MESSAGES['no_command'],
                             reply_markup=schedule_keyboard)
    else:
        await message.answer(HELP_MESSAGES['cant_talk'],
                             reply_markup=schedule_keyboard)


async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    logger.debug(LOGGER_MESSAGES['webhook_set'])


async def on_shutdown(dispatcher):
    session.close()
    await bot.delete_webhook()
    logger.debug(LOGGER_MESSAGES['shutdown'])


def main():
    start_webhook(
        dispatcher=dispatcher,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )


if __name__ == '__main__':
    main()
