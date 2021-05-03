import asyncio
import os
import json
import configparser
import logging.config
import logging.handlers
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from handlers.geo import register_handlers_geo

logger = logging.getLogger(__name__)


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


# Logger config
# def init_logger():
#     if not os.path.exists('logs'):
#         os.makedirs('logs')
#     with open("logging.json") as fp:
#         logging.config.dictConfig(json.load(fp))
#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/cancel", description="Отменить текущее действие"),
        BotCommand(command="/geo", description="Добавить геометку")
    ]
    await bot.set_my_commands(commands)


# config reader
def load_config(config_path):
    cfp = configparser.ConfigParser()
    cfp.read(config_path)
    config = AttrDict()
    for section in cfp.sections():
        config[section] = AttrDict()
        for key in cfp[section]:
            config[section][key] = cfp[section][key]
    return config


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    config = load_config('config.ini')
    bot = Bot(token=config.Telegram.token)
    dp = Dispatcher(bot, storage=MemoryStorage())
    register_handlers_geo(dp)
    await set_commands(bot)
    await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
