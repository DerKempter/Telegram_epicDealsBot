import logging
import os

from Handlers.handlers import get_bot
from Logic.logic import BotLogic

PORT = int(os.environ.get('PORT', 5000))

main_bot = BotLogic()
get_bot(main_bot)
logging.log(level=logging.INFO, msg='test')
main_bot.startup()
