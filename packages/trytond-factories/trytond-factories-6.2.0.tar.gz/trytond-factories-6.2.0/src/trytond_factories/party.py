
__all__ = [
    'PartyConfig',
    'SpanishVatcode',
    'Country',
    'PartyAddress',
    'PartyIdentifier',
    'PartyContact',
    'PhoneContact',
    'MobileContact',
    'FaxContact',
    'WebsiteContact',
    'EmailContact',
    'Party',
    'PartyAccount',
    'AccountInvoicePaymentTermLine',
    'AccountInvoicePaymentTerm',
    'ComParty',
]

import factory
import factory_trytond


class PartyConfig(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.configuration'

    party_lang = factory_trytond.ModelData('ir', 'lang_ca')
    party_sequence = factory.SubFactory(
        'trytond_factories.sequence.Sequence',
        name='Party',
        sequence_type=factory_trytond.ModelData(
            'party', 'sequence_type_party'),
    )


class SpanishVatcode(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.identifier'

    class Params:
        nif = factory.Faker('nif')

    code = factory.LazyAttribute('ES{.nif}'.format)


class Country(factory_trytond.TrytonFactory):
    class Meta:
        model = 'country.country'

    name = factory.Faker('country')
    code = factory.Faker('country_code')
    code3 = factory.Faker('pystr_format', string_format='???')
    code_numeric = factory.Faker('pystr_format', string_format='###')


class PartyAddress(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.address'

    name = factory.Faker('word')
    street = factory.Faker('street_address')
    city = factory.Faker('city')
    postal_code = factory.Faker('postcode')
    country = factory_trytond.LazySearch(
        'country.country', lambda stub: []
    )


class PartyIdentifier(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.identifier'

    code = factory.Faker('postcode')


class PartyContact(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.contact_mechanism'


class _PhoneNumberContact(PartyContact):
    value = factory.Faker('phone_number')


class PhoneContact(_PhoneNumberContact):
    type = 'phone'


class MobileContact(_PhoneNumberContact):
    type = 'mobile'


class FaxContact(_PhoneNumberContact):
    type = 'fax'


class WebsiteContact(PartyContact):
    type = 'website'
    value = factory.Faker('url')


class EmailContact(PartyContact):
    type = 'email'
    value = factory.Faker('email')


class Party(factory_trytond.TrytonFactory):

    class Meta:
        model = 'party.party'

    class Params:
        lang_code = factory.Faker('word', ext_word_list=['ca', 'es'])

    name = factory.Faker('name')
    identifiers = factory.RelatedFactoryList(
        PartyIdentifier,
        size=1,
        factory_related_name='party',
    )
    addresses = factory.RelatedFactoryList(
        PartyAddress,
        size=1,
        factory_related_name='party',
        invoice=True,
    )

    # Note that while the party.party pool model has
    # these very contact mechanism functional fields,
    # these identically named factory declarations are
    # "unrelated" to them in the sense that a RelatedFactory
    # will NOT attempt to use any functional setter or alike
    # but simply call XxxxContact.generate(party=instance)
    # in the instance post-generation stage, which will
    # utlimately show up in the parties' contact lists
    # and thus in the parties' functional contact fields.
    # Yet this is useful for the party factory usage as
    # Party.generate(fax=None, email__value='smbd@example.com')

    phone = factory.RelatedFactory(
        PhoneContact, factory_related_name='party'
    )
    mobile = factory.RelatedFactory(
        MobileContact, factory_related_name='party'
    )
    email = factory.RelatedFactory(
        EmailContact, factory_related_name='party'
    )
    fax = factory.RelatedFactory(
        FaxContact, factory_related_name='party'
    )
    website = factory.RelatedFactory(
        WebsiteContact, factory_related_name='party'
    )

    lang = factory_trytond.LazySearch(
        'ir.lang', lambda x: ['code', '=', x.lang_code])


class PartyAccount(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.party.account'


class AccountInvoicePaymentTermLine(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.invoice.payment_term.line'

    type = 'remainder'


class AccountInvoicePaymentTerm(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.invoice.payment_term'

    active = True
    name = factory.Faker('word')
    lines = factory.LazyFunction(
        lambda: [AccountInvoicePaymentTermLine.build()]
    )


class ComParty(Party):
    name = factory.Faker('company')
    customer_payment_term = factory.SubFactory(AccountInvoicePaymentTerm)
    accounts = factory.RelatedFactoryList(
        PartyAccount, size=1, factory_related_name='party',
    )
