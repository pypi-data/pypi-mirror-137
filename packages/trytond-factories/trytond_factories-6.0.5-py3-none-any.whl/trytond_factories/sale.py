
__all__ = [
    'SaleConfig',
    'SaleLine',
    'SaleSubtotal',
    'Sale',
]

import factory
import factory_trytond


class SaleConfig(factory_trytond.TrytonFactory):
    class Meta:
        model = 'sale.configuration'

    sale_sequence = factory.SubFactory(
        'trytond_factories.sequence.Sequence',
        name='Sale',
        sequence_type=factory_trytond.ModelData(
            'sale', 'sequence_type_sale'),
    )
    sale_invoice_method = 'shipment'


class _SaleLine(factory_trytond.TrytonFactory):
    class Meta:
        model = 'sale.line'


class SaleLine(_SaleLine):
    type = 'line'
    sale = None
    unit = factory.SelfAttribute('product.template.sale_uom')
    quantity = factory.Faker(
        'pyint',
        min_value=1,
        max_value=3,
    )
    unit_price = factory.Faker(
        'pyint',
        min_value=2,
        max_value=50,
        step=1,
    )
    product = factory.SubFactory('trytond_factories.product.Product')

    @classmethod
    def on_change(cls, obj):
        obj.on_change_product()


class SaleSubtotal(_SaleLine):
    type = 'subtotal'


class Sale(factory_trytond.TrytonFactory):
    class Meta:
        model = 'sale.sale'

    party = factory.SubFactory('trytond_factories.party.Party')
    invoice_party = factory.SelfAttribute('party')
    invoice_address = factory.LazyAttribute(
        lambda n: n.party.address_get('invoice')
    )

    @factory.post_generation
    def lines(obj, create, extracted, **kwargs):
        obj.lines = (
            extracted
            or SaleLine.create_batch(
                1,
                sale=obj,
                company=obj.company,
                **kwargs,
            )
        )

    @factory.post_generation
    def state(obj, create, extracted, **kwargs):
        "For example: Sale.create(state='cancel')"
        Model = obj.__class__
        state_transitions = {
            None: tuple(()),
            'draft': tuple(()),
            'quotation': (Model.quote,),
            'confirmed': (Model.quote, Model.confirm),
            'processing': (
                Model.quote,
                Model.confirm,
                Model.process,
            ),
            'cancel': (Model.cancel,),
        }
        return state_transitions[extracted]

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(Sale, cls)._after_postgeneration(obj, create, results)
        if create and results:
            for button in results['state']:
                button([obj])
