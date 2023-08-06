======================
Account Batch Scenario
======================

Imports::

    >>> import datetime
    >>> from dateutil.relativedelta import relativedelta
    >>> from decimal import Decimal
    >>> from proteus import config, Model, Wizard
    >>> from trytond.tests.tools import activate_modules
    >>> from trytond.modules.company.tests.tools import create_company, \
    ...     get_company
    >>> from trytond.modules.account.tests.tools import create_fiscalyear, \
    ...     create_chart, get_accounts
    >>> from trytond.modules.account_invoice.tests.tools import \
    ...     set_fiscalyear_invoice_sequences, create_payment_term
    >>> from trytond.modules.account_batch.tests.tools import \
    ...     create_tax, create_tax_code, create_tax_code_line
    >>> today = datetime.date.today()

Install account_batch::

    >>> config = activate_modules('account_batch')

Create company::

    >>> _ = create_company()
    >>> company = get_company()

Create fiscal year::

    >>> fiscalyear = set_fiscalyear_invoice_sequences(
    ...     create_fiscalyear(company))
    >>> fiscalyear.click('create_period')
    >>> fiscalyear.save()
    >>> period_ids = [p.id for p in fiscalyear.periods]
    >>> period = fiscalyear.periods[0]

Create chart of accounts::

    >>> _ = create_chart(company)
    >>> accounts = get_accounts(company)
    >>> revenue = accounts['revenue']
    >>> expense = accounts['expense']
    >>> receivable = accounts['receivable']
    >>> payable = accounts['payable']
    >>> cash = accounts['cash']
    >>> tax = accounts['tax']

Create tax groups::

    >>> TaxCode = Model.get('account.tax.code')
    >>> TaxGroup = Model.get('account.tax.group')

    >>> group_ust = TaxGroup()
    >>> group_ust.name = 'Ust.'
    >>> group_ust.code = 'ust'
    >>> group_ust.kind = 'sale'
    >>> group_ust.save()

    >>> group_vst = TaxGroup()
    >>> group_vst.name = 'Vst.'
    >>> group_vst.code = 'vst'
    >>> group_vst.kind = 'purchase'
    >>> group_vst.save()

Create taxes and tax codes: VAT Sale::

    >>> tax_out = create_tax('USt. 19%', Decimal('0.19'))
    >>> tax_out.group = group_ust
    >>> tax_out.save()

    >>> base19out = create_tax_code('Base Out', tax_out)
    >>> base19out.save()
    >>> base19out_line1 = create_tax_code_line(base19out, tax_out,
    ...     operator='+', type='invoice', amount='base')
    >>> base19out_line1.save()
    >>> base19out_line2 = create_tax_code_line(base19out, tax_out,
    ...     operator='-', type='credit', amount='base')
    >>> base19out_line2.save()
 
    >>> tax19out = create_tax_code('Tax Out', tax_out)
    >>> tax19out.save()
    >>> tax19out_line1 = create_tax_code_line(tax19out, tax_out,
    ...     operator='+', type='invoice', amount='tax')
    >>> tax19out_line1.save()
    >>> tax19out_line2 = create_tax_code_line(tax19out, tax_out,
    ...     operator='-', type='credit', amount='tax')
    >>> tax19out_line2.save()

Create taxes and tax codes: VAT Purchase::

    >>> tax_in = create_tax('VSt. 19%', Decimal('0.19'))
    >>> tax_in.group = group_vst
    >>> tax_in.save()

    >>> base19in = create_tax_code('Base In', tax_in)
    >>> base19in.save()
    >>> base19in_line1 = create_tax_code_line(base19in, tax_in,
    ...     operator='+', type='invoice', amount='base')
    >>> base19in_line1.save()
    >>> base19in_line2 = create_tax_code_line(base19in, tax_in,
    ...     operator='-', type='credit', amount='base')
    >>> base19in_line2.save()
 
    >>> tax19in = create_tax_code('Tax In', tax_in)
    >>> tax19in.save()
    >>> tax19in_line1 = create_tax_code_line(tax19in, tax_in,
    ...     operator='+', type='invoice', amount='tax')
    >>> tax19in_line1.save()
    >>> tax19in_line2 = create_tax_code_line(tax19in, tax_in,
    ...     operator='-', type='credit', amount='tax')
    >>> tax19in_line2.save()

Create taxes and tax codes: Nested VAT Intracommunity Purchase (Reverse Charge)::

    >>> tax_in_intra = create_tax('Steuerpflichtiger innergemeinschaftlicher Erwerb 19%', None, type='none')
    >>> tax_in_intra.group = group_vst
    >>> tax_in_intra.reverse_charge = True
    >>> tax_in_intra.save()

    >>> tax_in_intra_sub = create_tax('Innergem. Erwerb 19%USt/19%VSt', None, type='none')
    >>> tax_in_intra_sub.parent = tax_in_intra
    >>> tax_in_intra_sub.reverse_charge = True
    >>> tax_in_intra_sub.save()

    >>> tax_in_intra_sub_vst = create_tax('19% Vorsteuer aus innergem. Erwerb', Decimal('0.19'))
    >>> tax_in_intra_sub_vst.parent = tax_in_intra_sub
    >>> tax_in_intra_sub_vst.reverse_charge = True
    >>> tax_in_intra_sub_vst.save()

    >>> tax_in_intra_sub_ust = create_tax('19% Umsatzsteuer aus innergem. Erwerb', Decimal('-0.19'))
    >>> tax_in_intra_sub_ust.parent = tax_in_intra_sub
    >>> tax_in_intra_sub_ust.reverse_charge = True
    >>> tax_in_intra_sub_ust.save()

    >>> code_base19in_vst = create_tax_code(
    ...     'Vorsteuerbeträge aus dem innergemeinschaftlichen Erwerb von Gegenständen Netto (89)',
    ...     tax_in_intra_sub_vst)
    >>> code_base19in_vst.save()
    >>> code_base19in_vst_line1 = create_tax_code_line(code_base19in_vst, tax_in_intra_sub_vst,
    ...     operator='+', type='invoice', amount='base')
    >>> code_base19in_vst_line1.save()
    >>> code_base19in_vst_line2 = create_tax_code_line(code_base19in_vst, tax_in_intra_sub_vst,
    ...     operator='-', type='credit', amount='base')
    >>> code_base19in_vst_line2.save()

    >>> code_tax19in_vst = create_tax_code(
    ...     'Vorsteuerbeträge aus dem innergemeinschaftlichen Erwerb von Gegenständen Steuer (61)',
    ...     tax_in_intra_sub_vst)
    >>> code_tax19in_vst.save()
    >>> code_tax19in_vst_line1 = create_tax_code_line(code_tax19in_vst, tax_in_intra_sub_vst,
    ...     operator='+', type='invoice', amount='tax')
    >>> code_tax19in_vst_line1.save()
    >>> code_tax19in_vst_line2 = create_tax_code_line(code_tax19in_vst, tax_in_intra_sub_vst,
    ...     operator='-', type='credit', amount='tax')
    >>> code_tax19in_vst_line2.save()
 
    >>> code_tax19in_ust = create_tax_code(
    ...     'Steuerpflichtige innergemeinschaftliche Erwerbe Steuer (891)',
    ...     tax_in_intra_sub_ust)
    >>> code_tax19in_ust.save()
    >>> code_tax19in_ust_line1 = create_tax_code_line(code_tax19in_ust, tax_in_intra_sub_ust,
    ...     operator='+', type='invoice', amount='tax')
    >>> code_tax19in_ust_line1.save()
    >>> code_tax19in_ust_line2 = create_tax_code_line(code_tax19in_ust, tax_in_intra_sub_ust,
    ...     operator='-', type='credit', amount='tax')
    >>> code_tax19in_ust_line2.save()

Create taxes and tax codes: Nested VAT Sale (Reverse Charge)::

    >>> # While this tax is not really applicable in EU, it should also work just in case.

    >>> tax_out_intra = create_tax('Steuerpflichtige Lieferung Reverse Charge 19%', None, type='none')
    >>> tax_out_intra.group = group_ust
    >>> tax_out_intra.reverse_charge = True
    >>> tax_out_intra.save()

    >>> tax_out_intra_sub = create_tax('Lieferung Reverse Charge 19%VSt/19%USt', None, type='none')
    >>> tax_out_intra_sub.parent = tax_out_intra
    >>> tax_out_intra_sub.reverse_charge = True
    >>> tax_out_intra_sub.save()

    >>> tax_out_intra_sub_vst = create_tax('19% Vorsteuer aus innergem. Lieferung', Decimal('-0.19'))
    >>> tax_out_intra_sub_vst.parent = tax_out_intra_sub
    >>> tax_out_intra_sub_vst.reverse_charge = True
    >>> tax_out_intra_sub_vst.save()

    >>> tax_out_intra_sub_ust = create_tax('19% Umsatzsteuer aus innergem. Lieferung', Decimal('0.19'))
    >>> tax_out_intra_sub_ust.parent = tax_out_intra_sub
    >>> tax_out_intra_sub_ust.reverse_charge = True
    >>> tax_out_intra_sub_ust.save()

    >>> code_base19out_vst = create_tax_code(
    ...     'Vorsteuerbeträge aus der innergemeinschaftlichen Lieferung von Gegenständen Netto (89x)',
    ...     tax_out_intra_sub_vst)
    >>> code_base19out_vst.save()
    >>> code_base19out_vst_line1 = create_tax_code_line(code_base19out_vst, tax_out_intra_sub_vst,
    ...     operator='+', type='invoice', amount='base')
    >>> code_base19out_vst_line1.save()
    >>> code_base19out_vst_line2 = create_tax_code_line(code_base19out_vst, tax_out_intra_sub_vst,
    ...     operator='-', type='credit', amount='base')
    >>> code_base19out_vst_line2.save()

    >>> code_tax19out_vst = create_tax_code(
    ...     'Vorsteuerbeträge aus dem innergemeinschaftlichen Lieferung von Gegenständen Steuer (61x)',
    ...     tax_out_intra_sub_vst)
    >>> code_tax19out_vst.save()
    >>> code_tax19out_vst_line1 = create_tax_code_line(code_tax19out_vst, tax_out_intra_sub_vst,
    ...     operator='+', type='invoice', amount='tax')
    >>> code_tax19out_vst_line1.save()
    >>> code_tax19out_vst_line2 = create_tax_code_line(code_tax19out_vst, tax_out_intra_sub_vst,
    ...     operator='-', type='credit', amount='tax')
    >>> code_tax19out_vst_line2.save()
 
    >>> code_tax19out_ust = create_tax_code(
    ...     'Steuerpflichtige innergemeinschaftliche Lieferungen Steuer (891x)',
    ...     tax_out_intra_sub_ust)
    >>> code_tax19out_ust.save()
    >>> code_tax19out_ust_line1 = create_tax_code_line(code_tax19out_ust, tax_out_intra_sub_ust,
    ...     operator='+', type='invoice', amount='tax')
    >>> code_tax19out_ust_line1.save()
    >>> code_tax19out_ust_line2 = create_tax_code_line(code_tax19out_ust, tax_out_intra_sub_ust,
    ...     operator='-', type='credit', amount='tax')
    >>> code_tax19out_ust_line2.save()

Create sequence and account journal::

    >>> Sequence = Model.get('ir.sequence')
    >>> AccountJournal = Model.get('account.journal')

    >>> sequence = Sequence(name='Bank',
    ...     code='account.journal',
    ...     company=company,
    ... )
    >>> sequence.save()
    >>> account_journal = AccountJournal(name='Bank',
    ...     type='bank',
    ...     sequence=sequence,
    ... )
    >>> account_journal.save()     

Create parties::

    >>> Party = Model.get('party.party')
    >>> customer = Party(name='Customer')
    >>> customer.save()
    >>> supplier = Party(name='Supplier')
    >>> supplier.save()

Create payment term::

    >>> payment_term = create_payment_term()
    >>> payment_term.save()

Create a batch user::

    >>> User = Model.get('res.user')
    >>> Group = Model.get('res.group')
    >>> Party = Model.get('party.party')
    >>> Employee = Model.get('company.employee')
    >>> batch_user = User()
    >>> batch_user.name = 'Batch User'
    >>> batch_user.login = 'batch'
    >>> batch_user.main_company = company
    >>> batch_group, = Group.find([('name', '=', 'Batch')])
    >>> batch_user.groups.append(batch_group)
    >>> account_group, = Group.find([('name', '=', 'Account')])
    >>> batch_user.groups.append(account_group)
    >>> employee_party = Party(name="Batch Employee")
    >>> employee_party.save()
    >>> employee = Employee(party=employee_party)
    >>> employee.save()
    >>> batch_user.employees.append(employee)
    >>> batch_user.employee = employee
    >>> batch_user.save()

.. comment:: We either work as batch_admin or batch_user to check
   correct permission settings
   

Create a batch admin::

    >>> batch_admin = User()
    >>> batch_admin.name = 'Batch Admin'
    >>> batch_admin.login = 'batch_admin'
    >>> batch_admin.main_company = company
    >>> account_admin_group, = Group.find([('name', '=', 'Account Administration')])
    >>> batch_admin.groups.append(account_admin_group)
    >>> batch_admin.save()

Create a batch journal (without optional account)::

    >>> config.user = batch_admin.id
    >>> config._context = User.get_preferences(True, config.context)
    >>> BatchJournal = Model.get('account.batch.journal')

    >>> batch_journal = BatchJournal(name='Batch Bank',
    ...     account_journal=account_journal,
    ...     currency=company.currency,
    ...     company=company,
    ... )
    >>> batch_journal.save()

Create a batch and check for missing account on journal::

    >>> config.user = batch_user.id
    >>> config._context = User.get_preferences(True, config.context)
    >>> Batch = Model.get('account.batch')
    >>> batch = Batch(name='Testbatch',
    ...     journal=batch_journal,
    ... )  # doctest: +IGNORE_EXCEPTION_DETAIL 
    Traceback (most recent call last):
        ...
    UserError: ...

Create a batch after configuring the journal with an account::

    >>> config.user = batch_admin.id
    >>> config._context = User.get_preferences(True, config.context)
    >>> batch_journal.account = cash
    >>> batch_journal.save()
    >>> batch = Batch(name='Testbatch',
    ...     journal=batch_journal,
    ... )
    >>> batch.save()

Create a revenue batch line without tax::

    >>> config.user = batch_user.id
    >>> config._context = User.get_preferences(True, config.context)
    >>> BatchLine = Model.get('account.batch.line')
    >>> batch_line1 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(100),
    ...     account=cash,
    ...     contra_account=revenue,
    ... )
    >>> batch_line1.save()
    >>> batch_line1.side_account
    'debit'
    >>> batch_line1.side_contra_account
    'credit'
    >>> len(batch.lines)
    1
    >>> len(batch.move_lines)
    2
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('100.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('100.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Cancel the former line::

    >>> batch_line2 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(100),
    ...     contra_account=revenue,
    ...     account=cash,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line2.save()
    >>> batch_line2.is_cancelation_move
    1
    >>> batch_line2.side_account
    'debit'
    >>> batch_line2.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    2
    >>> len(batch.move_lines)
    4
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create an expense batch line without tax::

    >>> batch_line3 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-100),
    ...     account=cash,
    ...     contra_account=expense,
    ... )
    >>> batch_line3.save()
    >>> batch_line3.side_account
    'credit'
    >>> batch_line3.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    3
    >>> len(batch.move_lines)
    6
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('100.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Cancel the former line::

    >>> batch_line4 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-100),
    ...     account=cash,
    ...     contra_account=expense,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line4.save()
    >>> batch_line4.side_account
    'credit'
    >>> batch_line4.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    4
    >>> len(batch.move_lines)
    8
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create a revenue batch line with tax::

    >>> batch_line5 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out,
    ... )
    >>> batch_line5.save()
    >>> batch_line5.side_account
    'debit'
    >>> batch_line5.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    5
    >>> len(batch.move_lines)
    11
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('840.34')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('1000.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('840.34')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('159.66')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')


Cancel the former line::

    >>> batch_line6 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line6.save()
    >>> batch_line6.side_account
    'debit'
    >>> batch_line6.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    6
    >>> len(batch.move_lines)
    14
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create an expense batch line with tax::

    >>> batch_line7 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in,
    ... )
    >>> batch_line7.save()
    >>> batch_line7.side_account
    'credit'
    >>> batch_line7.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    7
    >>> len(batch.move_lines)
    17
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('840.34')
    >>> cash.reload()
    >>> cash.credit
    Decimal('1000.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('840.34')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('159.66')

Cancel the former line::

    >>> batch_line8 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line8.save()
    >>> batch_line8.side_account
    'credit'
    >>> batch_line8.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    8
    >>> len(batch.move_lines)
    20
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('0.00')
    >>> revenue.debit
    Decimal('0.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('0.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create 2 customer invoices::

    >>> Invoice = Model.get('account.invoice')
    >>> customer_invoice1 = Invoice(type='out')
    >>> customer_invoice1.party = customer
    >>> customer_invoice1.payment_term = payment_term
    >>> invoice_line = customer_invoice1.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('100')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_invoice1.click('post')
    >>> customer_invoice1.state
    'posted'

    >>> customer_invoice2 = Invoice(type='out')
    >>> customer_invoice2.party = customer
    >>> customer_invoice2.payment_term = payment_term
    >>> invoice_line = customer_invoice2.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('150')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_invoice2.click('post')
    >>> customer_invoice2.state
    'posted'

Create 1 customer credit note::

    >>> customer_credit_note = Invoice(type='out')
    >>> customer_credit_note.party = customer
    >>> customer_credit_note.payment_term = payment_term
    >>> invoice_line = customer_credit_note.lines.new()
    >>> invoice_line.quantity = -1
    >>> invoice_line.unit_price = Decimal('50')
    >>> invoice_line.account = revenue
    >>> invoice_line.description = 'Test'
    >>> customer_credit_note.click('post')
    >>> customer_credit_note.state
    'posted'

Create 1 supplier invoice::

    >>> supplier_invoice = Invoice(type='in')
    >>> supplier_invoice.party = supplier
    >>> supplier_invoice.payment_term = payment_term
    >>> invoice_line = supplier_invoice.lines.new()
    >>> invoice_line.quantity = 1
    >>> invoice_line.unit_price = Decimal('50')
    >>> invoice_line.account = expense
    >>> invoice_line.description = 'Test'
    >>> supplier_invoice.invoice_date = today
    >>> supplier_invoice.click('post')
    >>> supplier_invoice.state
    'posted'

Check for intermediate results::
 
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('50.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('0.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create a receivable batch line with a customer invoice::

    >>> customer_invoice1.account == receivable
    True
    >>> batch_line9 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_invoice1,
    ... )
    >>> batch_line9.save()
    >>> batch_line9.reload()
    >>> batch_line9.side_account
    'debit'
    >>> batch_line9.side_contra_account
    'credit'
    >>> batch_line9.contra_account == customer_invoice1.account
    True
    >>> batch_line9.amount == customer_invoice1.total_amount
    True
    >>> batch_line9.party == customer_invoice1.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    9
    >>> len(batch.move_lines)
    22
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('150.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('100.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create another receivable batch line with a second customer invoice::

    >>> customer_invoice2.account == receivable
    True
    >>> batch_line10 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_invoice2,
    ... )
    >>> batch_line10.save()
    >>> batch_line10.reload()
    >>> batch_line10.side_account
    'debit'
    >>> batch_line10.side_contra_account
    'credit'
    >>> batch_line10.contra_account == customer_invoice2.account
    True
    >>> batch_line10.amount == customer_invoice2.total_amount
    True
    >>> batch_line10.party == customer_invoice2.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    10
    >>> len(batch.move_lines)
    24
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('250.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('0.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create a receivable batch line with a customer credit note::

    >>> customer_credit_note.account == receivable
    True
    >>> batch_line11 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=customer_credit_note,
    ... )
    >>> batch_line11.save()
    >>> batch_line11.reload()
    >>> batch_line11.side_account
    'credit'
    >>> batch_line11.side_contra_account
    'debit'
    >>> batch_line11.contra_account == customer_credit_note.account
    True
    >>> batch_line11.amount == customer_credit_note.total_amount
    True
    >>> batch_line11.party == customer_credit_note.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    11
    >>> len(batch.move_lines)
    26
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('0.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('50.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create a payable batch line with a supplier invoice::

    >>> supplier_invoice.account == payable
    True
    >>> batch_line12 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     account=cash,
    ...     invoice=supplier_invoice,
    ... )
    >>> batch_line12.save()
    >>> batch_line12.reload()
    >>> batch_line12.side_account
    'credit'
    >>> batch_line12.side_contra_account
    'debit'
    >>> batch_line12.contra_account == supplier_invoice.account
    True
    >>> batch_line12.amount == supplier_invoice.total_amount * -1
    True
    >>> batch_line12.party == supplier_invoice.party
    True
    >>> batch.reload()
    >>> len(batch.lines)
    12
    >>> len(batch.move_lines)
    28
    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('50.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')

    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')

Create an expense batch line with nested tax::

    >>> batch_line13 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in_intra,
    ... )
    >>> batch_line13.save()
    >>> batch_line13.side_account
    'credit'
    >>> batch_line13.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    13
    >>> len(batch.move_lines)
    32
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('1050.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('1100.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('1000.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('190.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('-190.00')

Cancel the former line::

    >>> batch_line14 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(-1000),
    ...     account=cash,
    ...     contra_account=expense,
    ...     tax=tax_in_intra,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line14.save()
    >>> batch_line14.side_account
    'credit'
    >>> batch_line14.side_contra_account
    'debit'
    >>> batch.reload()
    >>> len(batch.lines)
    14
    >>> len(batch.move_lines)
    36
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('0.00')

Create a revenue batch line with nested tax::

    >>> batch_line15 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out_intra,
    ... )
    >>> batch_line15.save()
    >>> batch_line15.side_account
    'debit'
    >>> batch_line15.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    15
    >>> len(batch.move_lines)
    40
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('1050.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('1100.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_baseout_vst = TaxCode(code_base19out_vst.id)
    ...     code_baseout_vst.amount
    Decimal('1000.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_vst = TaxCode(code_tax19out_vst.id)
    ...     code_tax_out_vst.amount
    Decimal('-190.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_ust = TaxCode(code_tax19out_ust.id)
    ...     code_tax_out_ust.amount
    Decimal('190.00')

Cancel the former line::

    >>> batch_line16 = BatchLine(journal=batch_journal,
    ...     batch=batch,
    ...     date=today,
    ...     amount=Decimal(1000),
    ...     account=cash,
    ...     contra_account=revenue,
    ...     tax=tax_out_intra,
    ...     is_cancelation_move=True,
    ... )
    >>> batch_line16.save()
    >>> batch_line16.side_account
    'debit'
    >>> batch_line16.side_contra_account
    'credit'
    >>> batch.reload()
    >>> len(batch.lines)
    16
    >>> len(batch.move_lines)
    44
    >>> revenue.reload()
    >>> revenue.credit
    Decimal('250.00')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('50.00')
    >>> cash.reload()
    >>> cash.credit
    Decimal('100.00')
    >>> cash.debit
    Decimal('250.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_baseout_vst = TaxCode(code_base19out_vst.id)
    ...     code_baseout_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_vst = TaxCode(code_tax19out_vst.id)
    ...     code_tax_out_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_ust = TaxCode(code_tax19out_ust.id)
    ...     code_tax_out_ust.amount
    Decimal('0.00')


Post the batch::

    >>> Move = Model.get('account.move')
    >>> batch.click('close')
    >>> batch.state
    'closed'
    >>> customer_invoice1.reload()
    >>> customer_invoice1.state
    'paid'
    >>> customer_invoice2.reload()
    >>> customer_invoice2.state
    'paid'
    >>> customer_credit_note.reload()
    >>> customer_credit_note.state
    'paid'
    >>> supplier_invoice.reload()
    >>> supplier_invoice.state
    'paid'
    >>> batch.reload()
    >>> (len([ml for ml in batch.move_lines if ml.move_state == 'posted'])
    ...       == len(batch.move_lines))
    True

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_baseout_vst = TaxCode(code_base19out_vst.id)
    ...     code_baseout_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_vst = TaxCode(code_tax19out_vst.id)
    ...     code_tax_out_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_ust = TaxCode(code_tax19out_ust.id)
    ...     code_tax_out_ust.amount
    Decimal('0.00')

Use the cancelation wizard to cancel some posted batch lines::

    >>> wizard_cancel = Wizard('account.batch.cancel',
    ...     [batch_line1, batch_line3, batch_line5, batch_line7])
    >>> wizard_cancel.form.description = 'Continue'
    >>> wizard_cancel.execute('cancelation')
    >>> wizard_cancel.state
    'end'
    >>> batch.reload()
    >>> len(batch.lines)
    20
    >>> len(batch.move_lines)
    54

    >>> receivable.reload()
    >>> receivable.credit
    Decimal('300.00')
    >>> receivable.debit
    Decimal('300.00')
    >>> payable.reload()
    >>> payable.credit
    Decimal('50.00')
    >>> payable.debit
    Decimal('50.00')

    >>> revenue.reload()
    >>> revenue.credit
    Decimal('-690.34')
    >>> revenue.debit
    Decimal('50.00')
    >>> expense.reload()
    >>> expense.credit
    Decimal('0.00')
    >>> expense.debit
    Decimal('-890.34')

    >>> cash.reload()
    >>> cash.credit
    Decimal('-1000.00')
    >>> cash.debit
    Decimal('-850.00')

    >>> with config.set_context(periods=period_ids):
    ...     base19out = TaxCode(base19out.id)
    ...     base19out.amount
    Decimal('-840.34')
    >>> with config.set_context(periods=period_ids):
    ...     tax19out = TaxCode(tax19out.id)
    ...     tax19out.amount
    Decimal('-159.66')
    >>> with config.set_context(periods=period_ids):
    ...     base19in = TaxCode(base19in.id)
    ...     base19in.amount
    Decimal('-840.34')
    >>> with config.set_context(periods=period_ids):
    ...     tax19in = TaxCode(tax19in.id)
    ...     tax19in.amount
    Decimal('-159.66')
    >>> with config.set_context(periods=period_ids):
    ...     code_basein_vst = TaxCode(code_base19in_vst.id)
    ...     code_basein_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_vst = TaxCode(code_tax19in_vst.id)
    ...     code_tax_in_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_in_ust = TaxCode(code_tax19in_ust.id)
    ...     code_tax_in_ust.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_baseout_vst = TaxCode(code_base19out_vst.id)
    ...     code_baseout_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_vst = TaxCode(code_tax19out_vst.id)
    ...     code_tax_out_vst.amount
    Decimal('0.00')
    >>> with config.set_context(periods=period_ids):
    ...     code_tax_out_ust = TaxCode(code_tax19out_ust.id)
    ...     code_tax_out_ust.amount
    Decimal('0.00')
