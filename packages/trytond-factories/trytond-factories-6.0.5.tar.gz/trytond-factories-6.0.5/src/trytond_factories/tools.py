
__all__ = [
    'supress_user_warnings',
    'context_company',
    'context_user',
    'context_warehouse',
]

import contextlib
import factory
import unittest.mock

from trytond.pool import Pool
from trytond.transaction import Transaction


@contextlib.contextmanager
def supress_user_warnings():
    "Patch res.user.warning class to supress any user warning check"
    ResUserWarning = Pool().get('res.user.warning')
    with unittest.mock.patch.object(
            ResUserWarning,
            'check',
            return_value=False,
    ):
        yield


@factory.LazyFunction
def context_company():
    if rec_id := Transaction().context.get('company'):
        return Pool().get('company.company')(rec_id)


@factory.LazyFunction
def context_user():
    if rec_id := Transaction().user:
        return Pool().get('res.user')(rec_id)


@factory.LazyFunction
def context_warehouse():
    if rec_id := Transaction().context.get('warehouse'):
        return Pool().get('stock.location')(rec_id)
