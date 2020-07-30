import scrapy

import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader

from sqlalchemy.orm import sessionmaker

from FoodPandaStore.FoodPandaStore.model import *

from FoodPandaStore.FoodPandaStore.items import FoodpandastoreLine
import re
from urllib.parse import urljoin

from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join


import socket
import datetime as dt
from datetime import datetime, timezone

class FoodpandalatlongstoreSpider(scrapy.Spider):

    name = 'FoodPandaLtLnStore'
    allowed_domains = ['foodpanda.co.th']
    start_urls = ['https://www.foodpanda.co.th/']


    custom_settings = {
        'ITEM_PIPELINES': {
            'FoodPandaStore.pipelines.FoodpandastorePipeline': 100
        }
    }


    is_test = False
    test_latln = [{'TAM_ID':10193, 'AM_ID':1019, 'CH_ID':10, 'lat':6.546, 'ln':99.706},
                  {'TAM_ID':100103, 'AM_ID':1001, 'CH_ID':10, 'lat':13.75, 'ln':100.499}]




    def get_geo_location(self, session):
        '''
         List all of tambon's lat, long from TambonGeo
        '''

        try:
            # tambon = session().query(TambonGeo).filter_by(province_id=30).all()
            tambon = session().query(TambonGeo2.sub_district_id,
                                     TambonGeo2.sub_district_th,
                                     TambonGeo2.district_id,
                                     TambonGeo2.district_th,
                                     TambonGeo2.province_id,
                                     TambonGeo2.province_th,
                                     TambonGeo2.latitude,
                                     TambonGeo2.longitude).all()
            return tambon
        except Exception as e:
            self.logger.inf(e)


    def __init__(self, lang='th'):

        '''

        Prepare database session / connection
        '''

        self.lang = lang
        engine = db_connect()
        create_tables(engine)
        session = sessionmaker(bind=engine)
        self.tambon = self.get_geo_location(session)

    def start_requests(self):
        '''
        parsing request url format https://www.foodpanda.co.th/th/restaurants/lat/{lat}/lng/{ln}
        to search store on spiecific tambon.
        '''

        if self.is_test:
            for pos in self.test_latln:
                for start_url in self.start_urls:
                    lat = pos['lat']
                    long = pos['ln']
                    tam_id = pos['TAM_ID']
                    am_id = pos['AM_ID']
                    ch_id = pos['CH_ID']
                    url = "{}{}/restaurants/lat/{}/lng/{}?r=1".format(start_url, self.lang, lat, long)
                    yield Request(url=url, callback=self.vendor_parse, meta={'TAM_ID': tam_id,
                                                                             'AM_ID': am_id,
                                                                             'CH_ID': ch_id})
            return
        else:
            for pos in self.tambon:
                self.logger.info("{} / {} / {}".format(pos.sub_district_th, pos.district_th, pos.province_th))

                for start_url in self.start_urls:
                    url = "{}{}/restaurants/lat/{}/lng/{}?r=1".format(start_url,
                                                                       self.lang,
                                                                       pos.latitude,
                                                                       pos.longitude)
                    yield Request(url=url, callback=self.vendor_parse, meta={'TAM_ID': pos.sub_district_id,
                                                                             'AM_ID': pos.district_id,
                                                                             'CH_ID': pos.province_id})
            return


    def vendor_parse(self, response):
        '''
            crawl over online / offline store

        '''

        stores = response.xpath('//*[@class="vendor-list opened"]//*[@class="hreview-aggregate url"]')
        store_off = response.xpath('//*[@class="vendor-list closed"]//*[@class="hreview-aggregate url"]')


        for store in stores:

            pif = ItemLoader(item=FoodpandastoreLine(), response=response)

            pif.add_value('store_name',store.xpath('.//*[@class="name fn"]/text()').extract_first())
            pif.add_value('store_id',store.xpath('./@data-vendor-id').extract_first() )
            pif.add_value('store_tag',store.xpath('.//*[@class="vendor-characteristic"]/span/text()').extract())

            pif.add_value('store_rating',store.xpath('.//*[@class="ratings-component"]/*[@class="rating"]/strong/text()').extract_first(), float)
            pif.add_value('store_price_rating',
                          len([x for x in store.xpath('.//*[@class="categories summary"]/li/span/text()').extract_first() if x == "$"]),
                          int)
            pif.add_value('store_count_rating',
                          store.xpath('.//*[@class="ratings-component"]/*[@class="count"]/@data-count').extract_first(),
                          MapCompose(lambda x: re.findall('\d+',x), int))

            pif.add_value('store_info_url', store.xpath('./@href').extract())

            pif.add_value('store_ta_id',response.meta['TAM_ID'], int)
            pif.add_value('store_am_id',response.meta['AM_ID'], int)
            pif.add_value('store_ch_id',response.meta['CH_ID'], int)

            ## House Keeping
            pif.add_value('url', response.url)
            pif.add_value('project', self.settings.get('BOT_NAME'))
            pif.add_value('spider', self.name)
            pif.add_value('server', socket.gethostname())
            pif.add_value('date', dt.datetime.now(timezone.utc).astimezone().isoformat())
            yield pif.load_item()

            for store in store_off:
                pif = ItemLoader(item=FoodpandastoreLine(), response=response)

                pif.add_value('store_name', store.xpath('.//*[@class="name fn"]/text()').extract_first())
                pif.add_value('store_id', store.xpath('./@data-vendor-id').extract_first())
                pif.add_value('store_tag', store.xpath('.//*[@class="vendor-characteristic"]/span/text()').extract())

                pif.add_value('store_rating', store.xpath(
                    './/*[@class="ratings-component"]/*[@class="rating"]/strong/text()').extract_first(), float)
                pif.add_value('store_price_rating',
                              len([x for x in
                                   store.xpath('.//*[@class="categories summary"]/li/span/text()').extract_first() if
                                   x == "$"]),
                              int)
                pif.add_value('store_count_rating',
                              store.xpath(
                                  './/*[@class="ratings-component"]/*[@class="count"]/@data-count').extract_first(),
                              MapCompose(lambda x: re.findall('\d+', x), int))

                pif.add_value('store_info_url', store.xpath('./@href').extract())

                pif.add_value('store_ta_id', response.meta['TAM_ID'], int)
                pif.add_value('store_am_id', response.meta['AM_ID'], int)
                pif.add_value('store_ch_id', response.meta['CH_ID'], int)

                ## House Keeping
                pif.add_value('url', response.url)
                pif.add_value('project', self.settings.get('BOT_NAME'))
                pif.add_value('spider', self.name)
                pif.add_value('server', socket.gethostname())
                pif.add_value('date', dt.datetime.now(timezone.utc).astimezone().isoformat())
                yield pif.load_item()



###  https://www.foodpanda.co.th/th/restaurants/lat/6.546/lng/99.706ls
###  https://www.foodpanda.co.th/th/restaurants/lat/13.75/lng/100.499

## scrapy crawl  FoodPandaLtLnStore --loglevel=INFO -o test.csv
##&expedition_type=pickup

