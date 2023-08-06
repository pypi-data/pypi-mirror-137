
__all__ = [
    'UserWarning_',
    'User',
    'UserRole',

]

import factory
import factory_trytond

from . import context_user


class UserWarning_(factory_trytond.TrytonFactory):
    class Meta:
        model = 'res.user.warning'

    user = context_user
    name = factory.Faker('slug')
    always = False


class User(factory_trytond.TrytonFactory):
    class Meta:
        model = 'res.user'

    name = factory.Faker('name')
    login = factory.Faker('user_name')
    email = factory.Faker('ascii_company_email')
    password = factory.Faker('password', length=10)
    company = factory.SubFactory('trytond_factories.company.Company')
    companies = factory.LazyAttribute(lambda o: [o.company])
    employees = factory.LazyAttribute(lambda o: [o.employee])
    employee = factory.SubFactory(
        'trytond_factories.company.Employee',
        company=factory.LazyAttribute(lambda o: o.factory_parent.company),
    )
    warehouse = factory_trytond.ModelData('stock', 'location_warehouse')


class UserRole(factory_trytond.TrytonFactory):
    class Meta:
        model = 'res.user.role'

    from_date = factory.Faker('past_date')
    to_date = factory.Faker('future_date')
