
__all__ = [
    'Company',
    'Employee',
]

import factory
import factory_trytond


class Company(factory_trytond.TrytonFactory):
    class Meta:
        model = 'company.company'

    class Params:
        currency_code = None

    party = factory.SubFactory('trytond_factories.party.ComParty')
    currency = factory.Maybe(
        'currency_code',
        no_declaration=factory.SubFactory('trytond_factories.currency.Euro'),
        yes_declaration=factory_trytond.LazySearch(
            'currency.currency', lambda x: ['code', '=', x.currency_code]
        )
    )


class Employee(factory_trytond.TrytonFactory):
    class Meta:
        model = 'company.employee'

    party = factory.SubFactory('trytond_factories.party.Party')
    company = factory.SubFactory(Company)
