HELP_MESSAGES = {
    'start': 'Привет, я телеграм бот, который поможет тебе '
             'проверить расписание.\nДля того, чтобы увидеть '
             'все возможные команды, напиши /help',
    'help': 'Мои команды:\n/info - информация о '
            'выбранной группе\n/set_group - установить группу '
            'для выдачи расписания\n/get_schedule - получить расписание',
    'set_group': 'Для того чтобы получить расписание - напиши '
                 'номер группы в формате XX-12-13',
    'user_not_exist': 'Вы ещё не записали группу, для этого используйте '
                      'команду /set_group'
}

SCHEDULE_MESSAGE = ('Расписание на {day_of_week}, {date}:\n'
                    'Группа: {group}\n'
                    'Дисциплина: {discipline}\n'
                    'Тип занятия: {kind_of_work}\n'
                    'Начало занятия: {begin_lesson}\n'
                    'Конец занятия: {end_lesson}\n'
                    'Преподаватель: {lecturer}'
                    )
