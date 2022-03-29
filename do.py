def set_hook():
    import asyncio
    from telegram_bot.settings import (HEROKU_APP_NAME,
                                       WEBHOOK_URL,
                                       TELEGRAM_TOKEN)
    from aiogram import Bot
    bot = Bot(token=TELEGRAM_TOKEN)

    async def hook_set():
        if not HEROKU_APP_NAME:
            print('You have forgot to set HEROKU_APP_NAME')
            quit()
        await bot.set_webhook(WEBHOOK_URL)
        print(await bot.get_webhook_info())

    asyncio.run(hook_set())
    bot.close()


def start():
    from telegram_bot.bot_main import main
    main()


if __name__ == '__main__':
    start()
