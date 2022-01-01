import scrapy
from items import IsthereanydealItem
# from IsthereanydealItem.py import IsthereanydealItem
from scrapy.crawler import CrawlerProcess

# start_url='https://isthereanydeal.com/game/heartsofironiii/history/?stats1=all&stats2=all'
class IsthereanydealSpiderSpider(scrapy.Spider):
    name = 'isthereanydeal_spider'
    allowed_domains = ['isthereanydeal.com']
    # filename = open('/Volumes/GoogleDrive/My Drive/Python Projects/df_game_names_list_1.csv','r')
    # file = csv.DictReader(filename)

    # start_urls = ['https://isthereanydeal.com/game/runawayatwistoffate/history/?stats1=all&stats2=all']
    # df_game_names = pandas.read_csv('/Volumes/GoogleDrive/My Drive/Python Projects/scrapy_isthereanydeal/isthereanydeal/df_game_names.csv')
    # game_list = ['https://isthereanydeal.com/game/' + game + '/history/?stats1=all&stats2=all' for game in df_game_names.game_name]
    # start_urls = [
    #     # Testing list
    #     'https://isthereanydeal.com/game/heartsofironiii/history/?stats1=all&stats2=all'
    #     # 'https://isthereanydeal.com/game/bioshock/history/?stats1=all&stats2=all',
    #     # 'https://isthereanydeal.com/game/runawayatwistoffate/history/?stats1=all&stats2=all'
    #     # game_list
    # ]
    # for col in file:
    #    start_urls.append(col['url'])

    """Stores each items' individual components into an item container"""
    def parse(self, response):
        items = IsthereanydealItem()
        game_title = response.css('#gameTitle').extract()
        game_store_name = response.css('.shopTitle::text').extract()
        game_date = response.css('.lg2__time-rel::text').extract()
        game_regular_price = response.css('.show-801+ .lg2__price').css('::text').extract()
        game_actual_price = response.css('.lg2__price--new::text').extract()
        sale_duration = response.css('.lg2__time-rel i::text').extract()
        game_release_date = response.css('#gameHead__release').extract()

        items['game_title'] = game_title
        items['game_store_name'] = game_store_name
        items['game_date'] = game_date
        items['game_regular_price'] = game_regular_price
        items['game_actual_price'] = game_actual_price
        items['sale_duration'] = sale_duration
        items['game_release_date'] = game_release_date

        # Ensures all items are running properly
        yield items

