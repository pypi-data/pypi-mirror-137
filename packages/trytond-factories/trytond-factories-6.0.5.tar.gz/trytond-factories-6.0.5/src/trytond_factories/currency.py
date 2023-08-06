
__all__ = [
    'CurrencyRate',
    'BaseCurrency',
    'Euro',
    'OtherCurrency',
]

import datetime
from decimal import Decimal

import factory
import factory_trytond


class CurrencyRate(factory_trytond.TrytonFactory):
    class Meta:
        model = 'currency.currency.rate'

    date = factory.Faker('date_object')
    rate = factory.Faker(
        'pydecimal',
        min_value=0,
        max_value=10,
        right_digits=6,
    )


class _Currency(factory_trytond.TrytonFactory):
    class Meta:
        model = 'currency.currency'

    name = factory.Faker('currency_name')
    code = factory.Faker('currency_code')
    symbol = factory.Faker('currency_symbol')
    digits = factory.Faker('pyint', min_value=2, max_value=6)
    numeric_code = factory.Faker('pystr_format', string_format='###')
    rounding = factory.LazyAttribute(
        lambda stub: Decimal('1e-{.digits}'.format(stub)))


class BaseCurrency(_Currency):

    # https://docs.tryton.org/projects/modules-currency/en/latest/usage.html#setting-currency-exchange-rates

    base_rate = factory.RelatedFactory(
        CurrencyRate,
        factory_related_name='currency',
        rate=1,
        date=datetime.date.min,
    )


class Euro(BaseCurrency):
    name = 'Euro'
    code = 'EUR'
    symbol = '€'
    digits = 2


class OtherCurrency(_Currency):

    rates = factory.RelatedFactoryList(
        CurrencyRate, factory_related_name='currency', size=20)
