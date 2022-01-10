import datetime
import logging

import requests

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


def keep_up(bot):
    r = requests.request("https://api.telegram.org/bot5098403386:AAEp18hrFADbej9CkfK1Rs1e64cuummqglA/getMe")
    logging.log(level=logging.INFO, msg='Performing logging to keep the application awake')


def send_games(games_array, context, target_id: str):
    for game in games_array:
        context.bot.send_photo(chat_id=target_id, photo=game[1],
                               caption=f"{game[0]}\n"
                                       f"Original Prize: {game[2]}\n"
                                       f"On sale since {game[6]}\n"
                                       f"On sale until {game[7]}\n"
                                       f"<a href={game[4] + game[3]}>Store Link</a> \n"
                                       f"<a href={game[5] + game[3]}>Store Link</a> \n")


def get_free_games(update: Update, context: CallbackContext):
    global main_bot
    free_games = main_bot.get_free_games()
    target_id = update.effective_chat.id
    send_games(free_games, context, target_id)
    logging.log(level=logging.INFO, msg='executed "free" command')


def test_schedule(bot):
    bot.bot.send_message(chat_id=120147833, text="test")


def check_for_free_games(bot):
    with open("ids.txt", "r") as file:
        ids = file.readlines()
        ids = list(dict.fromkeys(ids))
        if "\n" in ids:
            ids.remove("\n")
    check_for_validity()
    with open("free_games.txt", "r+") as games_file:
        games = games_file.readlines()
        games = list(dict.fromkeys(games))
    for game in games:
        this_game = game.replace('\n', '').split('#')
        start_time: datetime.datetime = datetime.datetime.strptime(this_game[6], '%Y-%m-%d %H:%M:%S')
        end_time: datetime.datetime = datetime.datetime.strptime(this_game[7], '%Y-%m-%d %H:%M:%S')
        this_game[6] = start_time
        this_game[7] = end_time
        games.remove(game)
        games.append(this_game)
    global main_bot
    current_free_games = main_bot.get_free_games()
    for free_game in current_free_games:
        if free_game in games:
            current_free_games.remove(free_game)
    if len(current_free_games) > 0:
        save_free_games(current_free_games)
        for target_id in ids:
            send_games(current_free_games, bot, target_id.replace('\n', ''))
            logging.log(level=logging.INFO, msg='executed "check_free_games" command')
    else:
        logging.log(level=logging.INFO, msg='no new games found')
    logging.log(level=logging.INFO, msg='executed "check_for_free_games" command')


def save_free_games(free_games):
    game_strings = []
    for game in free_games:
        start_time_str = game[6].strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = game[7].strftime('%Y-%m-%d %H:%M:%S')
        game[6] = start_time_str
        game[7] = end_time_str
        game_string = '#'.join(game)
        game_strings.append(game_string)
    with open("free_games.txt", "a+") as saved_games:
        for string in game_strings:
            saved_games.write(string+"\n")
            logging.log(level=logging.INFO, msg='wrote a game to file')


def check_for_validity():
    with open("free_games.txt", "r+") as saved_games:
        games = saved_games.readlines()
    for game in games:
        game_array = game.replace('\n', '').split('#')
        end_time: datetime.datetime = datetime.datetime.strptime(game_array[7], '%Y-%m-%d %H:%M:%S')
        if end_time < datetime.datetime.now():
            games.remove(game)
            logging.log(level=logging.INFO, msg='removed a game from file_array')
    open("free_games.txt", "w").close()
    with open("free_games.txt", "r+") as saved_games:
        for game in games:
            saved_games.write(game)
            logging.log(level=logging.INFO, msg='wrote a game to file')


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


def unknown_command(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unknown Command :C")
    logging.log(level=logging.INFO, msg='executed "unknown" command')


start_handler = CommandHandler('start', start)
free_game_handler = CommandHandler('free', get_free_games)
subscribe_handler = CommandHandler('subscribe', register_for_free_games)
unsubscribe_handler = CommandHandler('unsub', unsubscribe_from_free_games)
unknown_handler = MessageHandler(Filters.command, unknown_command)


def get_handlers():
    res_list = [start_handler, free_game_handler, subscribe_handler, unsubscribe_handler, unknown_handler]
    return res_list
