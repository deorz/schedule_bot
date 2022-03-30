import datetime as dt

import aiohttp

from telegram_bot.messages import LOGGER_MESSAGES
from telegram_bot.settings import logger

timezone_offset = dt.timezone(dt.timedelta(hours=3))


async def get_json_from_api(url, group_id, begin_date, end_date):
    async with aiohttp.ClientSession() as session:
        endpoint_url = url.format(group_id=group_id,
                                  start_date=begin_date,
                                  finish_date=end_date)
        try:
            async with session.get(endpoint_url) as response:
                json = await response.json()
        except aiohttp.ClientConnectionError:
            logger.error(
                LOGGER_MESSAGES['endpoint_inaccessibility'].format(
                    endpoint_url))
        return json


def calculate_time(start_time=dt.datetime.now(tz=timezone_offset),
                   delta=0):
    start_time_str = start_time.strftime('%Y.%m.%d')
    delta = dt.timedelta(days=delta)
    end_time = start_time + delta
    end_time_str = end_time.strftime('%Y.%m.%d')
    return {
        'start_time_str': start_time_str,
        'end_time_str': end_time_str,
    }
