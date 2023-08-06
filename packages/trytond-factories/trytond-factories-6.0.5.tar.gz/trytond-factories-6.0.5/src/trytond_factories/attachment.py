
__all__ = [
    'DataAttachment',
    'LinkAttachment',
]

import factory
import factory_trytond


class _Attachment(factory_trytond.TrytonFactory):
    class Meta:
        model = 'ir.attachment'

    name = factory.Faker('word')
    description = factory.Faker('sentence')
    resource = factory.SubFactory('trytond_factories.test.TestModel')


class DataAttachment(_Attachment):
    class Meta:
        model = 'ir.attachment'

    type = 'data'
    data = factory.Faker('binary', length=64)
    file_id = factory.Faker('word')


class LinkAttachment(_Attachment):
    class Meta:
        model = 'ir.attachment'

    type = 'link'
    link = factory.Faker('uri')
