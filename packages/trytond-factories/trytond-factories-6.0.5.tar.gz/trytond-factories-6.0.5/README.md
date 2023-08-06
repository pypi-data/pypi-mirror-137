# Trytond-factories

Trytond-factories is a [factory_trytond](https://github.com/calidae/factory-trytond) extension which uses [factory_boy](https://factoryboy.readthedocs.io/en/latest/introduction.html) that allows to create [Tryton ERP](https://www.tryton.org/) models with factories.

You can inherit ERP's core model factories to do some testing or to populate databases with some sample data.

## How does it work?

Import this module and you will be able to create objects such as Company, Party, etc.

Here's an example with Tryton's model **Company**:
```python
import trytond_factories

company = trytond_factories.Company.create(party__name='Example Company')

print(company)
>>> Pool().get('company.company')(1)
```
