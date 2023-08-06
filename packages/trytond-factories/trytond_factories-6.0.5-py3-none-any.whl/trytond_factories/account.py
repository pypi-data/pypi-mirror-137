
__all__ = [
    'AccountChartTemplates',
    'AccountConfig',
    'FiscalYearSequence',
    'FiscalYear',
    'PercentTax',
    'FixedTax',
]

import datetime
import functools

import factory
import factory_trytond

from . import context_company


class AccountChartTemplates():

    class MinimalCA(factory.StubFactory):

        root = factory_trytond.ModelData('account', 'account_template_root_ca')  # noqa: E501
        receivable = factory_trytond.ModelData('account', 'account_template_receivable_ca')  # noqa: E501
        payable = factory_trytond.ModelData('account', 'account_template_payable_ca')  # noqa: E501
        revenue = factory_trytond.ModelData('account', 'account_template_revenue_ca')  # noqa: E501
        expense = factory_trytond.ModelData('account', 'account_template_expense_ca')  # noqa: E501
        tax = factory_trytond.ModelData('account', 'account_template_tax_ca')  # noqa: E501

    class MinimalEN(factory.StubFactory):

        root = factory_trytond.ModelData('account', 'account_template_root_en')  # noqa: E501
        receivable = factory_trytond.ModelData('account', 'account_template_receivable_en')  # noqa: E501
        payable = factory_trytond.ModelData('account', 'account_template_payable_en')  # noqa: E501
        revenue = factory_trytond.ModelData('account', 'account_template_revenue_en')  # noqa: E501
        expense = factory_trytond.ModelData('account', 'account_template_expense_en')  # noqa: E501
        tax = factory_trytond.ModelData('account', 'account_template_tax_en')  # noqa: E501

    class MinimalES(factory.StubFactory):

        root = factory_trytond.ModelData('account', 'account_template_root_es')  # noqa: E501
        receivable = factory_trytond.ModelData('account', 'account_template_receivable_es')  # noqa: E501
        payable = factory_trytond.ModelData('account', 'account_template_payable_es')  # noqa: E501
        revenue = factory_trytond.ModelData('account', 'account_template_revenue_es')  # noqa: E501
        expense = factory_trytond.ModelData('account', 'account_template_expense_es')  # noqa: E501
        tax = factory_trytond.ModelData('account', 'account_template_tax_es')  # noqa: E501

    class PGCNormal(factory.StubFactory):

        root = factory_trytond.ModelData('account_es', 'pgc_0_normal')
        receivable = factory_trytond.ModelData('account_es', 'pgc_4300_normal')
        payable = factory_trytond.ModelData('account_es', 'pgc_4000_normal')
        revenue = factory_trytond.ModelData('account_es', 'pgc_700_normal')
        expense = factory_trytond.ModelData('account_es', 'pgc_600_normal')
        tax = factory_trytond.ModelData('account_es', 'pgc_477_normal')

    class PGCPymes(factory.StubFactory):

        root = factory_trytond.ModelData('account_es', 'pgc_0_pymes')
        receivable = factory_trytond.ModelData('account_es', 'pgc_4300_pymes')
        payable = factory_trytond.ModelData('account_es', 'pgc_4000_pymes')
        revenue = factory_trytond.ModelData('account_es', 'pgc_700_pymes')
        expense = factory_trytond.ModelData('account_es', 'pgc_600_pymes')
        tax = factory_trytond.ModelData('account_es', 'pgc_477_pymes')


class AccountConfig(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.configuration'


class FiscalYearSequence(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.fiscalyear.invoice_sequence'

    company = context_company
    in_invoice_sequence = factory.SubFactory(
        'trytond_factories.sequence.StrictSequence',
        name='Supplier Invoice',
        sequence_type=factory_trytond.ModelData(
            'account_invoice', 'sequence_type_account_invoice'),
    )
    out_invoice_sequence = factory.SubFactory(
        'trytond_factories.sequence.StrictSequence',
        name='Customer Invoice',
        sequence_type=factory_trytond.ModelData(
            'account_invoice', 'sequence_type_account_invoice'),
    )
    in_credit_note_sequence = factory.SubFactory(
        'trytond_factories.sequence.StrictSequence',
        name='Supplier credit note',
        sequence_type=factory_trytond.ModelData(
            'account_invoice', 'sequence_type_account_invoice'),
    )
    out_credit_note_sequence = factory.SubFactory(
        'trytond_factories.sequence.StrictSequence',
        name='Customer credit note',
        sequence_type=factory_trytond.ModelData(
            'account_invoice', 'sequence_type_account_invoice'),
    )


class FiscalYear(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.fiscalyear'

    class Params:
        year = factory.LazyFunction(lambda: datetime.date.today().year)

    name = factory.LazyAttribute('{.year}'.format)
    start_date = factory.LazyAttribute(lambda o: datetime.date(o.year, 1, 1))
    end_date = factory.LazyAttribute(lambda o: datetime.date(o.year, 12, 31))
    post_move_sequence = factory.SubFactory(
        'trytond_factories.sequence.Sequence',
        sequence_type=factory_trytond.ModelData(
            'account', 'sequence_type_account_move'),
    )
    invoice_sequences = factory.LazyFunction(
        functools.partial(FiscalYearSequence.build_batch, 1)
    )

    @factory.post_generation
    def create_period(obj, create, extracted, **kwargs):
        return extracted is not False

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(FiscalYear, cls)._after_postgeneration(obj, create, results)
        if create and not obj.periods and results['create_period']:
            obj.create_period([obj])


class _Tax(factory_trytond.TrytonFactory):

    class Meta:
        model = 'account.tax'

    class Params:
        account_chart = factory.SubFactory(AccountChartTemplates.MinimalEN)
        invoice_account_tpl = factory.SelfAttribute('account_chart.tax')
        credit_note_account_tpl = factory.SelfAttribute('account_chart.tax')

    name = factory.Faker('word')
    description = factory.Faker('word')
    company = context_company
    invoice_account = factory_trytond.LazySearch(
        'account.account', lambda stub: [
            ('company', '=', stub.company),
            ('template', '=', stub.invoice_account_tpl),
        ]
    )

    credit_note_account = factory_trytond.LazySearch(
        'account.account', lambda stub: [
            ('company', '=', stub.company),
            ('template', '=', stub.credit_note_account_tpl),
        ]
    )


class PercentTax(_Tax):

    type = 'percentage'
    amount = None
    rate = factory.Faker(
        'pydecimal',
        positive=True,
        left_digits=0, right_digits=10,
    )


class FixedTax(_Tax):

    type = 'fixed'
    rate = None
    amount = factory.Faker(
        'pydecimal',
        positive=True,
        left_digits=1, right_digits=8,
    )
