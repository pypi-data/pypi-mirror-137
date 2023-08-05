# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import doctest
import unittest

from trytond.tests.test_tryton import (
    ModuleTestCase, doctest_checker, doctest_teardown)
from trytond.tests.test_tryton import suite as test_suite


class AccountTaxReverseChargeTestCase(ModuleTestCase):
    'Test Account Tax Reverse Charge module'
    module = 'account_tax_reverse_charge'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountTaxReverseChargeTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_account_tax_reverse_charge.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite
