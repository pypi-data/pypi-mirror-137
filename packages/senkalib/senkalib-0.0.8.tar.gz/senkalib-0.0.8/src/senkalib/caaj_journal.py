from typing import List

class CaajJournal:
  def __init__(self, time:str = None, transaction_id:str = None, comment:str = None, 
    debit_from:str = None, debit_to:str = None, credit_from:str = None, credit_to:str = None, 
    debit_title:str = None, debit_amount:dict = None, credit_title:str = None, credit_amount:dict = None):
    self.time = time
    self.transaction_id = transaction_id
    self.comment = comment  
    self.debit_from = debit_from
    self.debit_to = debit_to
    self.credit_from = credit_from
    self.credit_to = credit_to
    self.debit_title = debit_title
    self.debit_amount = debit_amount
    self.credit_title = credit_title
    self.credit_amount = credit_amount

  def set_caaj_meta(self, time:str, transaction_id:str, comment:str) -> dict:
    self.time = time
    self.transaction_id = transaction_id
    self.comment = comment

  def set_caaj_destination(self, debit_from:str, debit_to:str, credit_from:str, credit_to:str) -> dict:
    self.debit_from = debit_from
    self.debit_to = debit_to
    self.credit_from = credit_from
    self.credit_to = credit_to

  def set_caaj_value(self, debit_title:str, debit_amount:dict, credit_title:str, credit_amount:dict) -> dict:
    self.debit_title = debit_title
    self.debit_amount = debit_amount
    self.credit_title = credit_title
    self.credit_amount = credit_amount