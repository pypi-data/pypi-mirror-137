__all__ = [
    'TestModel',
]

import factory
import factory_trytond


class TestModel(factory_trytond.TrytonFactory):
    class Meta:
        model = 'test.model'

    name = factory.Faker('word')
