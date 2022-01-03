import logging

from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update

main_bot = None


def get_bot(bot):
    global main_bot
    main_bot = bot


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I respond to /free and show the current"
                                                                    " free epic games!")
    logging.log(level=logging.INFO, msg='executed "start" command')


def get_free_games(update: Update, context: CallbackContext):
    global main_bot
    free_games = main_bot.get_free_games()
    for game in free_games:
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=game[1],
                               caption=f"{game[0]}\n"
                                       f"Original Prize: {game[2]}\n"
                                       f"On sale since {game[6]}\n"
                                       f"On sale until {game[7]}\n"
                                       f"<a href={game[4] + game[3]}>Store Link</a> \n"
                                       f"<a href={game[5] + game[3]}>Store Link</a> \n")
    logging.log(level=logging.INFO, msg='executed "free" command')


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown Command :C")
    logging.log(level=logging.INFO, msg='executed "unknown" command')


start_handler = CommandHandler('start', start)
free_game_handler = CommandHandler('free', get_free_games)
unknown_handler = MessageHandler(Filters.command, unknown)


def get_handlers():
    res_list = [start_handler, free_game_handler, unknown_handler]
    return res_list
