from .journal_entries import JournalEntries
import logging

logger = logging.getLogger(__name__)


class AdvInterCompanyJournalEntries(JournalEntries):
    SIMPLE_FIELDS = [
        'memo',
        'tranDate',
        'tranId'
    ]

    RECORD_REF_FIELDS = [
        'class',
        'currency',
        'department',
        'location',
        'subsidiary',
        'toSubsidiary'
    ]

    TYPE_NAME = 'advInterCompanyJournalEntry'
