# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal

from proteus import Model

from trytond.modules.account.tests.tools import get_accounts
from trytond.modules.company.tests.tools import get_company

__all__ = ['create_tax', 'create_tax_code', 'create_tax_code_line']


def create_tax(name, rate, type='percentage', company=None, config=None):
    "Create a tax of rate"
    Tax = Model.get('account.tax', config=config)

    if not company:
        company = get_company()

    accounts = get_accounts(company)

    tax = Tax()
    tax.name = name
    tax.description = name
    if type is not None:
        tax.type = type
    if rate is not None:
        tax.rate = rate
    tax.invoice_account = accounts['tax']
    tax.credit_note_account = accounts['tax']
    return tax


def create_tax_code(name, tax, config=None):
    "Create a tax code for the tax"
    TaxCode = Model.get('account.tax.code', config=config)

    tax_code = TaxCode(name="Tax Code %s" % name)
    tax_code.company = tax.company
    return tax_code


def create_tax_code_line(tax_code, tax, amount='tax', type='invoice',
        operator='+', config=None):
    "Create a tax code line for the tax code"
    TaxCodeLine = Model.get('account.tax.code.line', config=config)

    line = TaxCodeLine()
    line.code = tax_code
    line.operator = operator
    line.tax = tax
    line.amount = amount
    line.type = type
    return line
