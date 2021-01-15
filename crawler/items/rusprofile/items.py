import scrapy
from itemloaders.processors import Compose, TakeFirst

from crawler.items.rusprofile.utilits import (
    is_active_org, dates_extractor, addr, name
)


class RusprofileItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    status_organization = scrapy.Field(output_processor=TakeFirst(),
                                       input_processor=Compose(is_active_org))
    ogrn = scrapy.Field(output_processor=TakeFirst())
    ogrn_date_from = scrapy.Field(output_processor=TakeFirst(),
                                  input_processor=Compose(dates_extractor))
    date_of_register = scrapy.Field(output_processor=TakeFirst(),
                                    input_processor=Compose(dates_extractor))
    law_address = scrapy.Field(output_processor=TakeFirst(),
                               input_processor=Compose(addr))
    owner = scrapy.Field(output_processor=TakeFirst(),
                         input_processor=Compose(name))
    owner_date_from = scrapy.Field(output_processor=TakeFirst(),
                                   input_processor=Compose(dates_extractor))
    inn_number = scrapy.Field(output_processor=TakeFirst())
    kpp_number = scrapy.Field(output_processor=TakeFirst())
    authorized_capital = scrapy.Field(output_processor=TakeFirst())
    primary_occupation = scrapy.Field(output_processor=TakeFirst(),
                                      input_processor=
                                      Compose(lambda t: ' '.join(t).strip()))
    primary_occupation_code = scrapy.Field(output_processor=TakeFirst())
    tax_authority = scrapy.Field(output_processor=TakeFirst())
    tax_authority_date_from = scrapy.Field(output_processor=TakeFirst(),
                                           input_processor=
                                           Compose(dates_extractor))
    okpo = scrapy.Field(output_processor=TakeFirst())
    okato = scrapy.Field(output_processor=TakeFirst())
    oktmo = scrapy.Field(output_processor=TakeFirst())
    okfs = scrapy.Field(output_processor=TakeFirst())
    okogu = scrapy.Field(output_processor=TakeFirst())
    # nested fields
    requisites = scrapy.Field()




