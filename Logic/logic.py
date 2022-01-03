import logging
import Handlers.handlers as handlers

from telegram.ext import Updater


def setup_logging():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def prep_token() -> str:
    with open("token.txt", "r") as file:
        token = file.readlines()
    return token[0]


class BotLogic:
    updater = None
    dispatcher = None
    token_string = None

    def __init__(self):
        setup_logging()
        prep_token()
        self.prep_dispatcher()

    def startup(self):
        self.updater.start_polling()
        self.updater.idle()

    def prep_dispatcher(self):
        token_string = prep_token()

        self.updater = Updater(token=token_string, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.dispatcher.add_handler(handlers.start_handler)
        self.dispatcher.add_handler(handlers.test_handler)
        self.dispatcher.add_handler(handlers.unknown_handler)
        return self.dispatcher

    def get_dispatcher(self):
        if self.dispatcher is not None:
            return self.dispatcher
        else:
            return self.prep_dispatcher()
