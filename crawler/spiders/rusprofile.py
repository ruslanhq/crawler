from urllib.parse import urlparse

from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items.rusprofile.requisites import (
    InfoFss, InfoMsp, InfoFnsItem, InfoPfrItem
)

from ..items.rusprofile.items import RusprofileItem


class RusprofSpider(CrawlSpider):
    name = 'rusprof'
    allowed_domains = ['rusprofile.ru']
    start_url = 'https://www.rusprofile.ru/search?query={query}' \
                '&type=ul&search_inactive=2'

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="main"]/div/div[2]/'
                                            'div[2]/div/div[2]/ul/li[12]/a',)),
             follow=True),
        Rule(LinkExtractor(allow='id/'), callback='main_parse'),
    )

    def __init__(self, query, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not query:
            raise Exception('A idi nahui!')

        self.start_urls = [self.start_url.format(query=query)]

    def main_parse(self, response):
        _request_url = urlparse(response.url)
        id_org = _request_url.path.strip('/id/')

        loader = ItemLoader(item=RusprofileItem(), response=response)
        loader.add_value('id', id_org)
        loader.add_xpath('title', '//div[@class="company-name"]/text()')
        loader.add_xpath('status_organization',
                         '//*[@id="anketa"]/div[1]/div/div[2]/span/text()')
        loader.add_xpath('status_organization',
                         '//*[@id="anketa"]/div[1]/div[1]/div[2]/text()')
        loader.add_xpath('ogrn', '//*[@id="clip_ogrn"]/text()')
        loader.add_xpath('ogrn_date_from',
                         '//*[@id="anketa"]/div[2]/div[1]/div[1]/div[1]/dl[1]/'
                         'dd[2]/text()')
        loader.add_xpath('date_of_register',
                         '//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[1]/'
                         'dd/text()')
        loader.add_xpath('law_address',
                         '//*[@id="anketa"]/div[2]/div[1]/div[2]/address/span'
                         '/text()')
        loader.add_xpath('owner',
                         '//*[@id="anketa"]/div[2]/div[1]/div[3]/span[3]/a/span'
                         '/text()')
        loader.add_xpath('owner',
                         '//div[@class="company-row hidden-parent"]'
                         '//span[@class="company-info__text"]/text()')
        loader.add_xpath('owner_date_from',
                         '//*[@id="anketa"]/div[2]/div[1]/div[3]/span[4]'
                         '/text()')
        loader.add_xpath('inn_number', '//*[@id="clip_inn"]/text()')
        loader.add_xpath('kpp_number', '//*[@id="clip_kpp"]/text()')
        loader.add_xpath('authorized_capital',
                         '//*[@id="anketa"]/div[2]/div[1]/div[1]/div[2]/dl[2]'
                         '/dd/span/text()')
        loader.add_xpath('primary_occupation',
                         '//*[@id="anketa"]/div[2]/div[2]/div[1]/span[2]'
                         '/text()')
        loader.add_xpath('primary_occupation_code',
                         '//*[@id="anketa"]/div[2]/div[2]/div[1]/span[2]'
                         '/span/text()')
        loader.add_xpath('tax_authority',
                         '//*[@id="anketa"]/div[2]/div[2]/div[2]/span[2]'
                         '/text()')
        loader.add_xpath('tax_authority_date_from',
                         '//*[@id="anketa"]/div[2]/div[2]/div[2]/span[3]'
                         '/text()')
        loader.add_xpath('okpo', '//*[@id="clip_okpo"]/text()')
        loader.add_xpath('okato', '//*[@id="clip_okato"]/text()')
        loader.add_xpath('oktmo', '//*[@id="clip_oktmo"]/text()')
        loader.add_xpath('okfs', '//*[@id="clip_okfs"]/text()')
        loader.add_xpath('okogu', '//*[@id="clip_okogu"]/text()')

        requisites = f'https://www.rusprofile.ru/requisites/{id_org}'
        yield response.follow(requisites, callback=self.parse_requisites,
                              meta={'organize': loader})

    def parse_requisites(self, response):
        organize = response.meta['organize']
        ex_f = response.xpath('//*[@id="main"]/div/div[2]/div[2]/div/div[5]'
                              '/text()').extract()[0]

        def parse_fns():
            loader = ItemLoader(item=InfoFnsItem(), response=response)
            loader.add_value('type', 'ФНС')
            loader.add_xpath('ogrn', '//*[@id="clip_ogrn_fns"]/text()')
            loader.add_xpath('date', '//*[@id="main"]/div/div[2]/div[2]'
                                     '/div/ul[3]/li[2]/div[2]/text()')
            loader.add_xpath('registrar', '//*[@id="main"]/div/div[2]/div[2]'
                                          '/div/ul[3]/li[3]/div[2]/text()')
            loader.add_xpath('address', '//*[@id="main"]/div/div[2]/div[2]/'
                                        'div/ul[3]/li[4]/div[2]/text()')
            return loader.load_item()

        def parse_pfr():
            q = 4 if ex_f == 'Внебюджетные фонды' else 5

            loader = ItemLoader(item=InfoPfrItem(), response=response)
            loader.add_value('type', 'ПФР')
            loader.add_xpath('reg_number', '//*[@id="clip_pfr_num"]/text()')
            loader.add_xpath('date', '//*[@id="main"]/div/div[2]/div[2]/div/'
                                     f'ul[{q}]/li[2]/div[2]/text()')
            loader.add_xpath('name', '//*[@id="main"]/div/div[2]/div[2]/div/'
                                     f'ul[{q}]/li[3]/div[2]/text()')
            return loader.load_item()

        def parse_fss():
            q = 5 if ex_f == 'Внебюджетные фонды' else 6

            loader = ItemLoader(item=InfoFss(), response=response)
            loader.add_value('type', 'ФСС')
            loader.add_xpath('reg_number', '//*[@id="clip_fss_num"]/text()')
            loader.add_xpath('date', '//*[@id="main"]/div/div[2]/div[2]/div/'
                                     f'ul[{q}]/li[2]/div[2]/text()')
            loader.add_xpath('name', '//*[@id="main"]/div/div[2]/div[2]/div/'
                                     f'ul[{q}]/li[3]/div[2]/text()')
            return loader.load_item()

        def parse_msp():
            q = 6 if ex_f == 'Внебюджетные фонды' else 7

            loader = ItemLoader(item=InfoMsp(), response=response)
            loader.add_value('type', 'МСП')
            loader.add_xpath('date', '//*[@id="main"]/div/div[2]/div[2]/div/'
                                     f'ul[{q}]/li[1]/div[2]/text()')
            loader.add_xpath('category', '//*[@id="main"]/div/div[2]/div[2]/'
                                         f'div/ul[{q}]/li[2]/div[2]/text()')
            return loader.load_item() if loader.get_collected_values('date')\
                else None

        requisites = list(filter(
            lambda func: func is not None,
            [parse_fns(), parse_pfr(), parse_fss(), parse_msp()]
        ))

        organize.add_value('requisites', requisites)
        yield organize.load_item()

