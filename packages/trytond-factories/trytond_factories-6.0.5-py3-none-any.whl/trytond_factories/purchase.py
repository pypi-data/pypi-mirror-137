
__all__ = [
    'PurchaseLine',
    'PurchaseSubtotal',
    'Purchase',
    'PartyPurchasePriceList',
]

import factory
import factory_trytond


class _PurchaseLine(factory_trytond.TrytonFactory):
    class Meta:
        model = 'purchase.line'


class PurchaseLine(_PurchaseLine):
    type = 'line'
    purchase = None
    unit = factory.SelfAttribute('product.template.purchase_uom')
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


class PurchaseSubtotal(_PurchaseLine):
    type = 'subtotal'


class Purchase(factory_trytond.TrytonFactory):
    class Meta:
        model = 'purchase.purchase'

    party = factory.SubFactory('trytond_factories.party.Party')
    invoice_address = factory.LazyAttribute(
        lambda n: n.party.address_get('invoice')
    )

    @factory.post_generation
    def lines(obj, create, extracted, **kwargs):
        obj.lines = (
            extracted
            or PurchaseLine.create_batch(
                1,
                purchase=obj,
                company=obj.company,
                **kwargs,
            )
        )

    @factory.post_generation
    def state(obj, create, extracted, **kwargs):
        "For example: Purchase.create(state='cancel')"
        Model = obj.__class__
        state_transitions = {
            None: tuple(()),
            'draft': tuple(()),
            'quotation': (Model.quote,),
            'confirmed': (Model.quote, Model.confirm),
            'processing': (Model.quote, Model.confirm, Model.process),
            'cancel': (Model.cancel),
        }
        return state_transitions[extracted]

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(Purchase, cls)._after_postgeneration(obj, create, results)
        if create and results:
            for button in results['state']:
                button([obj])


class PartyPurchasePriceList(factory_trytond.TrytonFactory):
    class Meta:
        model = 'party.party.purchase_price_list'

    party = None
    purchase_price_list = factory.SubFactory(
            'trytond_factories.product.PriceList')
