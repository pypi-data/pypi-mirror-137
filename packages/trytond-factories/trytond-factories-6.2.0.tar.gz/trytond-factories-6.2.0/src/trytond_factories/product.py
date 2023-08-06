
__all__ = [
    'ProductCategory',
    'ProductCategoryTree',
    'ProductAccountCategory',
    'ProductSupplier',
    'Product',
    'ProductTemplate',
    'PriceListLine',
    'PriceList',
]

import random

import factory
import factory_trytond

from trytond.pool import Pool


class ProductCategory(factory_trytond.TrytonFactory):
    class Meta:
        model = 'product.category'

    name = factory.Faker('word')


class ProductCategoryTree(ProductCategory):

    class Meta:
        model = 'product.category'

    childs = factory.RelatedFactoryList(
        ProductCategory,
        factory_related_name='parent',
        size=lambda: random.randint(2, 4),
        childs=factory.RelatedFactoryList(
            ProductCategory,
            factory_related_name='parent',
            size=lambda: random.randint(2, 4),
        )
    )


class ProductAccountCategory(ProductCategory):
    class Params:
        account_config = factory.LazyFunction(
            lambda: Pool().get('account.configuration').get_singleton()
        )

    accounting = True
    account_revenue = factory.LazyAttribute(
        lambda o: o.account_config.default_category_account_revenue)
    account_expense = factory.LazyAttribute(
        lambda o: o.account_config.default_category_account_expense)
    # TODO: taxes


class _Product(factory_trytond.TrytonFactory):
    class Meta:
        model = 'product.product'

    suffix_code = factory.Faker('pystr_format', string_format='#?')
    cost_price = factory.Faker(
        'pydecimal', min_value=10, max_value=100, right_digits=2)


class ProductSupplier(factory_trytond.TrytonFactory):
    class Meta:
        model = 'purchase.product_supplier'

    party = factory.SubFactory('trytond_factories.party.Party')


class _ProductTemplate(factory_trytond.TrytonFactory):
    class Meta:
        model = 'product.template'

    name = factory.Faker('word')
    code = factory.Faker('pystr_format', string_format='?###?')

    salable = True
    purchasable = True

    list_price = factory.Faker(
        'pydecimal', min_value=100, max_value=1000, right_digits=2)

    account_category = factory.SubFactory(ProductAccountCategory)

    product_suppliers = factory.RelatedFactoryList(
        ProductSupplier,
        factory_related_name='template',
        size=2,
    )


class Product(_Product):

    template = factory.SubFactory(
        _ProductTemplate,
    )


class ProductTemplate(_ProductTemplate):

    products = factory.RelatedFactoryList(
        _Product,
        factory_related_name='template',
        size=lambda: random.randint(1, 5),
    )


class PriceListLine(factory_trytond.TrytonFactory):
    class Meta:
        model = 'product.price_list.line'

    price_list = None
    product = factory.SubFactory(Product)
    formula = 'unit_price'


class PriceList(factory_trytond.TrytonFactory):
    class Meta:
        model = 'product.price_list'

    name = factory.Faker('word')
