import unittest
from senkalib.caaj_journal import CaajJournal

class TestCaajJounal(unittest.TestCase):
  def test_get_caaj_meta(self):
    cj = CaajJournal()
    caaj_meta = cj.set_caaj_meta('2022-01-12 11:11:11', '0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6', 'hello world')
    assert cj.time == '2022-01-12 11:11:11'
    assert cj.transaction_id == '0x36512c7e09e3570dfc53176252678ee9617660550d36f4da797afba6fc55bba6'
    assert cj.comment == 'hello world'

  def test_get_caaj_destination(self):
    cj = CaajJournal()
    caaj_destination = cj.set_caaj_destination(
      '0x111111111111111111111', 
      '0x222222222222222222222', 
      '0x333333333333333333333', 
      '0x444444444444444444444')
    assert cj.debit_from == '0x111111111111111111111'
    assert cj.debit_to == '0x222222222222222222222'
    assert cj.credit_from == '0x333333333333333333333'
    assert cj.credit_to == '0x444444444444444444444'

  def test_get_caaj_value(self):
    cj = CaajJournal()
    caaj_value = cj.set_caaj_value('LEND', {'USDT': '1000'}, 'SPOT', {'USDT': '1000'})
    assert cj.debit_title == 'LEND'
    assert cj.debit_amount == {'USDT': '1000'}
    assert cj.credit_title == 'SPOT'
    assert cj.credit_amount == {'USDT': '1000'}

if __name__ == '__main__':
  unittest.main()