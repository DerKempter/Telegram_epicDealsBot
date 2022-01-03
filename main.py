import logging

from Logic.logic import BotLogic

bot = BotLogic()
logging.log(level=logging.INFO, msg='test')
bot.startup()
