
__all__ = [
    'Sequence',
    'StrictSequence',
]

import factory
import factory_trytond


class _Sequence(factory_trytond.TrytonFactory):
    class Meta:
        abstract = True

    name = factory.Faker('word')
    prefix = factory.Faker('pystr', max_chars=1)
    suffix = factory.Faker('pystr', max_chars=1)
    padding = 5


class Sequence(_Sequence):
    class Meta:
        model = 'ir.sequence'


class StrictSequence(_Sequence):
    class Meta:
        model = 'ir.sequence.strict'
