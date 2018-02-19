from enum import Enum
from collections import namedtuple

Side = Enum('Side', 'BORROW LEND')

Order = namedtuple('Order', 'id party side term rate principle leaves')

g_id = 0

def new_order(party, side, principle, term, rate):
  global g_id
  g_id += 1
  return Order(g_id, party, side, term, rate, principle, principle)

