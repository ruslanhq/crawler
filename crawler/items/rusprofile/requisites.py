import scrapy
from itemloaders.processors import Compose, TakeFirst

from crawler.items.rusprofile.utilits import dates_extractor, addr


class InfoFnsItem(scrapy.Item):
    type = scrapy.Field(output_processor=TakeFirst())
    ogrn = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst(),
                        input_processor=Compose(dates_extractor))
    registrar = scrapy.Field(output_processor=TakeFirst())
    address = scrapy.Field(output_processor=TakeFirst(),
                           input_processor=Compose(addr))


class InfoPfrItem(scrapy.Item):
    type = scrapy.Field(output_processor=TakeFirst())
    reg_number = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst(),
                        input_processor=Compose(dates_extractor))
    name = scrapy.Field(output_processor=TakeFirst())


class InfoFss(scrapy.Item):
    type = scrapy.Field(output_processor=TakeFirst())
    reg_number = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst(),
                        input_processor=Compose(dates_extractor))
    name = scrapy.Field(output_processor=TakeFirst())


class InfoMsp(scrapy.Item):
    type = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field(output_processor=TakeFirst(),
                        input_processor=Compose(dates_extractor))
    category = scrapy.Field(output_processor=TakeFirst())
