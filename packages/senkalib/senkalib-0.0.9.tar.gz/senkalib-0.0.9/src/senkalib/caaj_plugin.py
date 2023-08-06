from abc import ABCMeta, abstractmethod
from senkalib.caaj_journal import CaajJournal
from senkalib.chain.transaction import Transaction
from typing import List

class CaajPlugin(metaclass=ABCMeta):
  chain = None

  @abstractmethod
  def can_handle(cls, transaction:Transaction) -> bool:
    pass

  @abstractmethod
  def get_caajs(cls, address:str, transaction:Transaction) -> List[CaajJournal]:
    pass