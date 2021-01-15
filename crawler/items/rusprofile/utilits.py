from enum import Enum
from natasha import DatesExtractor, MorphVocab, NamesExtractor, AddrExtractor
from datetime import date


morph_vocab = MorphVocab()
extractor = DatesExtractor(morph_vocab)
name_extractor = NamesExtractor(morph_vocab)
add_Extractor = AddrExtractor(morph_vocab)

address_kw_mapper = {
    'страна': 'country',
    'республика': 'republic',
    'область': 'region',
    'город': 'city',
    'деревня': 'village',
    'проспект': 'big_street',
    'индекс': 'zip',
    'край': 'territory',
    'улица': 'street',
    'посёлок': 'township',
    'переулок': 'lane',
    'дом': 'number_house',
    'строение': 'structure',
    'офис': 'office',
    'квартира': 'flat',
    'проезд': 'passage',
    'корпус': 'housing',
    'площадь': 'square',
    'шоссе': 'highway',
    'село': 'village',
    'бульвар': 'boulevard',
    'автономный округ': 'autonomous region',
    'набережная': 'embankment',
    None: 'unknown'
}


class StatusOrg(Enum):
    operating = (1, "Действующая организация")
    is_liquidation = (2, "Организация в процессе ликвидации")
    liquidated = (3, "Организация ликвидирована")
    process_of_bankruptcy = (4, 'Организация в процессе банкротства')
    process_of_reorganization = (5, 'Организация в процессе реорганизации')

    def __init__(self, id, title):
        self.id = id
        self.title = title


def addr(value):
    payload = {}
    instance = add_Extractor.find(str(value))
    fact = instance.fact
    for part in fact.parts:
        payload[address_kw_mapper[part.type]] = part.value
    return payload


def name(value):
    if not value:
        return ''
    instance = name_extractor.find(str(value))
    fact = instance.fact
    fact = {'first': fact.first, 'last': fact.last, 'middle': fact.middle}
    return fact


def dates_extractor(value):
    if not value:
        return ''
    instance = list(extractor(str(value)))
    fact = instance[0].fact
    date_obj = date(year=fact.year, month=fact.month, day=fact.day)
    return date_obj.isoformat()


def is_active_org(value):
    status = StatusOrg
    if value:
        for org in status:
            if value[0] == org.title:
                return org.id

