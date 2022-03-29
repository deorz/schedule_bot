import datetime as dt
import locale

import aiohttp


async def get_json_from_api(url, group_id, begin_date, end_date):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                url.format(group_id=group_id,
                           start_date=begin_date,
                           finish_date=end_date)) as response:
            json = await response.json()
        return json


def calculate_time(start_time=dt.datetime.now(), delta=0):
    locale.setlocale(locale.LC_TIME, "ru_RU")
    start_time_str = start_time.strftime('%Y.%m.%d')
    day_now = start_time.strftime('%a')
    delta = dt.timedelta(days=delta)
    end_time = start_time + delta
    end_time_str = end_time.strftime('%Y.%m.%d')
    return {
        'start_time_str': start_time_str,
        'end_time_str': end_time_str,
        'day_now': day_now
    }
