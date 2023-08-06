# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Table

from trytond import backend
from trytond.model import DeactivableMixin, ModelSQL, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction


class BatchJournal(DeactivableMixin, ModelSQL, ModelView):
    'Batch Journal'
    __name__ = 'account.batch.journal'

    name = fields.Char('Name', required=True)
    account_journal = fields.Many2One('account.journal', 'Account Journal',
            required=True)
    currency = fields.Many2One('currency.currency', 'Currency', required=True)
    company = fields.Many2One('company.company', 'Company', required=True)
    account = fields.Many2One('account.account', "Account",
        domain=[
            ('type', '!=', None),
            ('closed', '!=', True),
            ('company', '=', Eval('company')),
            ],
        depends=['company'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().connection.cursor()
        table = TableHandler(cls, module_name)
        sql_table = cls.__table__()
        journal_account = Table('account_journal_account')

        created_account = not table.column_exist('account')

        super(BatchJournal, cls).__register__(module_name)

        # Migration from 4.8: new account field
        if created_account and table.table_exist('account_journal_account'):
            value = journal_account.select(journal_account.credit_account,
                where=((journal_account.journal == sql_table.journal) &
                    (journal_account.credit_account ==
                        journal_account.debit_account)))
            # Don't use UPDATE FROM because SQLite does not support it.
            cursor.execute(*sql_table.update([sql_table.account], [value]))

    @staticmethod
    def default_currency():
        Company = Pool().get('company.company')
        if Transaction().context.get('company'):
            company = Company(Transaction().context['company'])
            return company.currency.id

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class Journal(metaclass=PoolMeta):
    __name__ = 'account.journal'

    @classmethod
    def __setup__(cls):
        super(Journal, cls).__setup__()
        cls.type.selection.append(('bank', 'Bank'))
