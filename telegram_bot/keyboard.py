from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_set_group = KeyboardButton('/set_group')
button_group = KeyboardButton('/group')
button_help = KeyboardButton('/help')
button_get_schedule = KeyboardButton('/get_schedule')

schedule_keyboard = ReplyKeyboardMarkup().row(button_set_group,
                                              button_group).add(
    button_get_schedule).add(button_help)
