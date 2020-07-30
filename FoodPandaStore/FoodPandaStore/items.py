# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Identity, Join



class FoodpandastoreLine(scrapy.Item):

    store_name = scrapy.Field(output_processor=TakeFirst())
    store_id = scrapy.Field(output_processor=TakeFirst())
    store_tag = scrapy.Field(output_processor=Join(','))
    store_rating = scrapy.Field(output_processor=TakeFirst())
    store_price_rating = scrapy.Field(output_processor=TakeFirst())
    store_count_rating = scrapy.Field(output_processor=TakeFirst())
    store_info_url = scrapy.Field(output_processor=TakeFirst())


    store_ta_id = scrapy.Field(output_processor=TakeFirst())
    store_am_id = scrapy.Field(output_processor=TakeFirst())
    store_ch_id = scrapy.Field(output_processor=TakeFirst())


    ### House Keeping
    url = scrapy.Field(output_processor=TakeFirst())
    project = scrapy.Field(output_processor=TakeFirst())
    spider = scrapy.Field(output_processor=TakeFirst())
    server = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst())


class FoodpandastoreInfo(scrapy.Item):

    pass


