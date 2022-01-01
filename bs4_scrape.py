from bs4 import BeautifulSoup
import requests
from game_map import GameMap

class Scrape:
    def get_key(val):
        """
        Checks to ensure the game has a key from game_map.py's dictionary of games
        """
        for key, value in GameMap.game_map.items():
            if val == value:
                return key
        return "Game doesn't exist"

    def scrape(game):
        """
        Scrapes game data and prices from the specified game
        """

        if Scrape.get_key(game) == "Game doesn't exist":
            return "Game doesn't exist"
        else:
            response = requests.get('https://isthereanydeal.com/game/'+Scrape.get_key(game)+'/history/?stats1=all&stats2=all')
            soup = BeautifulSoup(response.content, 'html.parser')

            game_title = [i.text for i in soup.select('#gameTitle')]
            game_date = [i.text for i in soup.select('.lg2__time-rel')]
            game_store_name = [i.text for i in soup.select('.shopTitle')]
            game_regular_price = [i.text for i in soup.select('.show-801+ .lg2__price')]
            game_actual_price = [i.text for i in soup.select('.lg2__price--new')]
            sale_duration = [i.text for i in soup.select('.lg2__time-rel i')]
            game_release_date = [i.text for i in soup.select('#gameHead__release')]

            """Create dataframe from the scraped data"""
            game_dict = {'game_title':game_title,
                         'game_date':game_date,
                         'game_store_name':game_store_name,
                         'game_regular_price':game_regular_price,
                         'game_actual_price':game_actual_price,
                         'sale_duration':sale_duration,
                         'game_release_date':game_release_date}

            return game_dict