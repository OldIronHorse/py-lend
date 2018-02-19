from enum import Enum
from collections import namedtuple

Side = Enum('Side', 'BORROW LEND')

Order = namedtuple('Order', 'party side term rate principle leaves')

def new_order(party, side, principle, term, rate):
  return Order(party, side, term, rate, principle, principle)
