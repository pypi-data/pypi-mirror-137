# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import doctest
import unittest

from trytond.tests.test_tryton import (
    ModuleTestCase, doctest_checker, doctest_setup, doctest_teardown)
from trytond.tests.test_tryton import suite as test_suite


class AccountBatchTestCase(ModuleTestCase):
    'Test Account Batch module'
    module = 'account_batch'


def suite():
    suite = test_suite()
    #suite.addTests(doctest.DocFileSuite(
    #        'scenario_account_batch.rst',
    #        setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
    #        checker=doctest_checker,
    #        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    suite.addTests(doctest.DocFileSuite(
            'scenario_account_batch_tax_cash.rst',
            setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,))
    #optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    # Run this test after the scenario, because the scenario needs a fresh
    # database. SQLite doesn't seem to properly rollback the transaction.
    # s. a. https://bugs.tryton.org/issue9133
    #suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
    #        AccountBatchTestCase))
    return suite
