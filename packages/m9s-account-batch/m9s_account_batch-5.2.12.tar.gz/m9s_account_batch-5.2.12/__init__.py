# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool

from . import batch, invoice, journal, move, party

__all__ = ['register']


def register():
    Pool.register(
        journal.Journal,
        journal.BatchJournal,
        batch.Batch,
        batch.BatchLine,
        batch.CancelBatchLinesAskSure,
        batch.CancelBatchLinesAskProblem,
        batch.OpenBatchJournalAsk,
        move.Move,
        move.MoveLine,
        module='account_batch', type_='model')
    Pool.register(
        batch.BatchLineTaxCash,
        invoice.Invoice,
        depends=['account_tax_cash'],
        module='account_batch', type_='model')
    Pool.register(
        batch.CancelBatchLines,
        batch.OpenBatchJournal,
        batch.PostBatchLines,
        party.PartyReplace,
        module='account_batch', type_='wizard')
