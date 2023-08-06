# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.account_batch.tests.test_account_batch import suite
except ImportError:
    from .test_account_batch import suite

__all__ = ['suite']
