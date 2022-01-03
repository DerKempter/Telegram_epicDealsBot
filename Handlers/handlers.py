import logging

from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    logging.log(level=logging.INFO, msg='executed "start" command')


def test(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Das ist ein test :D")
    logging.log(level=logging.INFO, msg='executed "test" command')


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown Command :C")
    logging.log(level=logging.INFO, msg='executed "unknown" command')


start_handler = CommandHandler('start', start)
test_handler = CommandHandler('test', test)
unknown_handler = MessageHandler(Filters.command, unknown)


def get_handlers():
    res_list = [start_handler, test_handler, unknown_handler]
    return res_list
