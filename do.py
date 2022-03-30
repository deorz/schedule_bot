def set_hook():
    import asyncio

    from aiogram import Bot

    from telegram_bot.settings import (TELEGRAM_TOKEN, WEBHOOK_URL,
                                       variables_check)
    bot = Bot(token=TELEGRAM_TOKEN)

    async def hook_set():
        variables_check()
        await bot.set_webhook(WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from telegram_bot.bot_main import main
    main()


if __name__ == '__main__':
    start()
