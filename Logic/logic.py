import logging
from datetime import datetime, time

import Handlers.handlers as handlers
from epicstore_api import EpicGamesStoreAPI
from telegram.ext import Updater, JobQueue, CallbackContext


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
    handler_list = None
    job_queue = None

    def __init__(self):
        setup_logging()
        prep_token()
        self.prep_dispatcher()
        self.prep_job_queue()

    def startup(self):
        self.updater.start_polling()
        self.updater.idle()

    def prep_job_queue(self):
        self.job_queue = self.updater.job_queue
        self.job_queue.set_dispatcher(dispatcher=self.dispatcher)
        self.job_queue.run_daily(callback=handlers.check_for_free_games, time=time(2, 28))

    def prep_dispatcher(self):
        token_string = prep_token()

        self.updater = Updater(token=token_string, use_context=True)
        self.dispatcher = self.updater.dispatcher

        self.handler_list = handlers.get_handlers()
        for handler in self.handler_list:
            self.dispatcher.add_handler(handler)

        return self.dispatcher

    def get_dispatcher(self):
        if self.dispatcher is not None:
            return self.dispatcher
        else:
            return self.prep_dispatcher()

    # noinspection PyMethodMayBeStatic
    def get_free_games(self) -> []:
        api = EpicGamesStoreAPI()
        free_games = api.get_free_games()['data']['Catalog']['searchStore']['elements']
        free_games_parsed = []
        for game in free_games:
            if game['promotions'] is None or game['price']['totalPrice']['fmtPrice']['discountPrice'] != '0':
                continue
            game_name = game['title']
            game_thumb = None

            for image in game['keyImages']:
                if image['type'] == 'Thumbnail':
                    game_thumb = image['url']
            game_price = game['price']['totalPrice']['fmtPrice']['originalPrice']
            page_slug = game['urlSlug']
            page_url_base = f"https://www.epicgames.com/store/p/"
            page_url_launcher_base = "http://epicfreegames.net/redirect?slug="

            start_date = None
            end_date = None
            try:
                game_promotions = game['promotions']['promotionalOffers']
                upcoming_promotions = game['promotions']['upcomingPromotionalOffers']
                if not game_promotions and upcoming_promotions:
                    # Promotion is not active yet, but will be active soon.
                    promotion_data = upcoming_promotions[0]['promotionalOffers'][0]
                    start_date_iso, end_date_iso = (
                        promotion_data['startDate'][:-1], promotion_data['endDate'][:-1]
                    )
                    # Remove the last "Z" character so Python's datetime can parse it.
                    start_date = datetime.fromisoformat(start_date_iso)
                    end_date = datetime.fromisoformat(end_date_iso)
                    # Will be free from start_date to end_date
                else:
                    promotion_data = game_promotions[0]['promotionalOffers'][0]
                    start_date_iso, end_date_iso = (
                        promotion_data['startDate'][:-1], promotion_data['endDate'][:-1]
                    )
                    start_date = datetime.fromisoformat(start_date_iso)
                    end_date = datetime.fromisoformat(end_date_iso)
                    # Is free now
            except TypeError:
                pass
            current_free_game = [game_name, game_thumb, game_price, page_slug, page_url_base, page_url_launcher_base,
                                 start_date, end_date]
            free_games_parsed.append(current_free_game)
        return free_games_parsed
