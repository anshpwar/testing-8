import unittest

from erpkit import consumer_78, contract


class ArchiveTests(unittest.TestCase):
    def test_archive_row(self):
        self.assertEqual(consumer_78.archive_row(contract.Record("SM-5", 1, "open")), "SM-5")
