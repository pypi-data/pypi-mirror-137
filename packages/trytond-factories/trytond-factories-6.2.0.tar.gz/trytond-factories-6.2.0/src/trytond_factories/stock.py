
__all__ = [
    'StorageLocation',
    'Warehouse',
    'StockConfig',
    'StockMove',
    'FoundStock',
    'ShipmentIn',
    'PurchaseShipment',
]

import functools
import operator

import factory
import factory_trytond

from . import context_warehouse


class _StockLocation(factory_trytond.TrytonFactory):
    class Meta:
        model = 'stock.location'

    name = factory.Faker('word')
    code = factory.Faker('pystr_format', string_format='???')


class StorageLocation(_StockLocation):
    type = 'storage'


class Warehouse(_StockLocation):
    type = 'warehouse'
    name = factory.Faker('city')
    code = factory.Faker('pystr_format', string_format='E###.## - T####')

    input_location = factory.SubFactory(
        StorageLocation,
        name=factory.LazyAttribute('Entrada {.factory_parent.name}'.format),
        code=factory.LazyAttribute('E-{.factory_parent.code}'.format),
    )
    storage_location = factory.SubFactory(
        StorageLocation,
        name=factory.LazyAttribute('Interior {.factory_parent.name}'.format),
        code=factory.LazyAttribute('I-{.factory_parent.code}'.format),
    )
    output_location = factory.SubFactory(
        StorageLocation,
        name=factory.LazyAttribute('Sortida {.factory_parent.name}'.format),
        code=factory.LazyAttribute('S-{.factory_parent.code}'.format),
    )


class StockConfig(factory_trytond.TrytonFactory):
    class Meta:
        model = 'stock.configuration'


class StockMove(factory_trytond.TrytonFactory):
    class Meta:
        model = 'stock.move'

    product = factory.SubFactory('trytond_factories.product.Product')
    quantity = factory.Faker('pyfloat')

    @classmethod
    def on_change(cls, obj):
        obj.on_change_product()

    @factory.post_generation
    def state(obj, create, extracted, **kwargs):
        "For example: StockMove.create(state='cancelled')"
        Model = obj.__class__
        state_transitions = {
            None: tuple(()),
            'draft': tuple(()),
            'assigned': (Model.assign,),
            # FIXME: how to reach 'staging' state?
            'done': (Model.do,),
            'cancelled': (Model.cancel,),
        }
        return state_transitions[extracted]

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(StockMove, cls)._after_postgeneration(obj, create, results)
        if create and results:
            for button in results['state']:
                button([obj])


class FoundStock(StockMove):

    warehouse = context_warehouse
    from_location = factory_trytond.ModelData('stock', 'location_lost_found')
    to_location = factory.SelfAttribute('warehouse.storage_location')


class ShipmentIn(factory_trytond.TrytonFactory):

    class Meta:
        model = 'stock.shipment.in'

    @factory.post_generation
    def state(obj, create, extracted, **kwargs):
        "For example: ShipmentIn.create(state='done')"
        Model = obj.__class__
        state_transitions = {
            None: tuple(()),
            'draft': tuple(()),
            'received': (Model.receive,),
            'done': (Model.receive, Model.done,),
            'cancel': (Model.cancel,),
        }
        return state_transitions[extracted]

    @classmethod
    def _after_postgeneration(cls, obj, create, results=None):
        super(ShipmentIn, cls)._after_postgeneration(obj, create, results)
        if create and results:
            for button in results['state']:
                button([obj])


class PurchaseShipment(ShipmentIn):

    class Params:
        purchase = None

    supplier = factory.SelfAttribute('purchase.party')
    warehouse = factory.SelfAttribute('purchase.warehouse')

    @factory.lazy_attribute
    def incoming_moves(stub):
        return functools.reduce(
            operator.concat,
            (line.moves for line in stub.purchase.lines)
        )
