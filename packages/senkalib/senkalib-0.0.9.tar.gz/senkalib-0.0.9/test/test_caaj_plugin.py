import unittest
from unittest.mock import *
from senkalib.caaj_plugin import CaajPlugin
from senkalib.chain.transaction import Transaction
from senkalib.caaj_journal import CaajJournal
from typing import List

class SampleCaajPlugin(CaajPlugin):
  @classmethod
  def can_handle(cls, transaction:Transaction):
    return True

  @classmethod
  def get_caajs(cls, address:str, transaction:Transaction) -> List[CaajJournal]:
    jounal = CaajJournal()
    return [jounal]

class TestCaajPlugin(unittest.TestCase):
  def test_cat_handle(self):
    result = SampleCaajPlugin.can_handle('XXXXXXXXXXXXXXXXXXXXXXX')
    assert result == True

  def test_get_caajs(self):
    result = SampleCaajPlugin.get_caajs('0x1111111111111111', None)
    assert type(result[0]) == CaajJournal

if __name__ == '__main__':
  unittest.main()