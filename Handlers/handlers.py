import datetime
import logging

from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from telegram import Update

import Logic.logic

main_bot = Logic.logic.BotLogic


def get_bot(bot):
    global main_bot
    main_bot = bot


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, I respond to /free and show the current"
                                                                    " free epic games!"
                                                                    "Type /subscribe to get updates on free games "
                                                                    "and /unsub to unsubscribe from updates.")
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


def check_for_free_games(context: CallbackContext) -> None:
    with open("ids.txt", "r") as file:
        ids = file.readlines()
        ids = list(dict.fromkeys(ids))
        if "\n" in ids:
            ids.remove("\n")
    for client in ids:
        context.bot.send_message(chat_id=client, text="testtesttest")
        logging.log(level=logging.INFO, msg='executed "check_free_games" command')


def register_for_free_games(update: Update, context: CallbackContext):
    chat_id_to_save = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id_to_save, text=f"saving id {chat_id_to_save}")
    with open("ids.txt", "a+") as file:
        file.seek(0)
        ids = file.readlines()
    ids = list(dict.fromkeys(ids))
    if "\n" in ids:
        ids.remove("\n")
    if f"{chat_id_to_save}\n" in ids:
        context.bot.send_message(chat_id=chat_id_to_save, text=f"you are already registered for updates")
        context.bot.send_message(chat_id=chat_id_to_save, text=f"unsubscribe with /unsub")
    else:
        ids.append(chat_id_to_save)
        context.bot.send_message(chat_id=chat_id_to_save, text=f"Saved id {chat_id_to_save} to database")
    open("ids.txt", "w").close()
    with open("ids.txt", "a+") as file:
        for id_nr in ids:
            file.write(f"{id_nr}\n")
    logging.log(level=logging.INFO, msg='executed "sub" command')


def unsubscribe_from_free_games(update: Update, context: CallbackContext):
    chat_id_to_remove = update.effective_chat.id
    with open("ids.txt", "a+") as file:
        file.seek(0)
        ids = file.readlines()
    ids = list(dict.fromkeys(ids))
    if "\n" in ids:
        ids.remove("\n")
    if f"{chat_id_to_remove}\n" not in ids:
        context.bot.send_message(chat_id=chat_id_to_remove, text=f"you are already unsubscribed from updates")
        context.bot.send_message(chat_id=chat_id_to_remove, text=f"subscribe with /subscribe")
    else:
        ids.remove(f"{chat_id_to_remove}\n")
        context.bot.send_message(chat_id=chat_id_to_remove, text=f"Removed id {chat_id_to_remove} from database")
    open("ids.txt", "w").close()
    with open("ids.txt", "a+") as file:
        for id_nr in ids:
            file.write(f"{id_nr}\n")
    logging.log(level=logging.INFO, msg='executed "unsub" command')


def unknown(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown Command :C")
    logging.log(level=logging.INFO, msg='executed "unknown" command')


start_handler = CommandHandler('start', start)
free_game_handler = CommandHandler('free', get_free_games)
subscribe_handler = CommandHandler('subscribe', register_for_free_games)
unsubscribe_handler = CommandHandler('unsub', unsubscribe_from_free_games)
unknown_handler = MessageHandler(Filters.command, unknown)


def get_handlers():
    res_list = [start_handler, free_game_handler, subscribe_handler, unsubscribe_handler, unknown_handler]
    return res_list
