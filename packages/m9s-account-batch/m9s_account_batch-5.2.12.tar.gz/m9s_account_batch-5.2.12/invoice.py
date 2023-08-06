# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def _update_tax_cash_basis(cls, invoices):
        if Transaction().context.get('skip_update_cash_basis'):
            return
        super()._update_tax_cash_basis(invoices)
