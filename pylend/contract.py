from collections import namedtuple

from .order import Side
from .exceptions import TermMismatchError, SideMismatchError

Contract = namedtuple('Contract', 'lend borrow term rate principle')

def new_contract(borrow, lend):
  if borrow.side != Side.BORROW or lend.side != Side.LEND:
    raise SideMismatchError
  if lend.term != borrow.term:
    raise TermMismatchError
  contract_amount = min(borrow.leaves, lend.leaves)
  return Contract(
    principle=contract_amount,
    rate=(borrow.rate + lend.rate) / 2,
    borrow=borrow._replace(leaves=borrow.leaves - contract_amount),
    lend=lend._replace(leaves=lend.leaves - contract_amount),
    term=lend.term
  )

def completed_orders(contract):
  return {o for o in [contract.borrow, contract.lend] if o.leaves == 0}
