import scrapy


class FoundersRusprofileItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    is_liquidate = scrapy.Field()
    part_money = scrapy.Field()
    part_percentile = scrapy.Field()
    president_commission = scrapy.Field()
    law_address = scrapy.Field()
    inn = scrapy.Field()
    ogrn = scrapy.Field()
    date_register = scrapy.Field()
