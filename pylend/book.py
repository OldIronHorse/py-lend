from collections import namedtuple

from .order import Side
from .contract import new_contract
from .exceptions import TermMismatchError

Book = namedtuple('Book', 'term lends borrows')

def new_book(term):
  return Book(term=term, lends=[], borrows=[])

def add_lend(book, lend):
  return book._replace(lends=sorted(book.lends + [lend],
                                    key=lambda b: b.rate))

def add_borrow(book, borrow):
  return book._replace(borrows=sorted(book.borrows + [borrow], 
                                      key=lambda b: b.rate * -1))

adders = {
  Side.BORROW: add_borrow,
  Side.LEND: add_lend,
}

def add_order(book, order):
  if book.term != order.term:
    raise TermMismatchError
  return adders[order.side](book, order);

def cross(book):
  try:
    if book.borrows[0].rate >= book.lends[0].rate:
      contract = new_contract(book.borrows[0], book.lends[0])
      new_borrows = book.borrows[1:]
      if contract.borrow.leaves > 0:
        new_borrows = [contract.borrow] + new_borrows
      new_lends = book.lends[1:]
      if contract.lend.leaves > 0:
        new_lends = [contract.lend] + new_lends
      return (book._replace(borrows=new_borrows, lends=new_lends),  contract)
  except IndexError:
    pass
  return (book, None)

def cross_all(book):
  contracts = []
  while True:
    book, contract = cross(book)
    if contract is None:
      break
    contracts.append(contract)
  return (book, contracts)

def cancel_order(book, order_id):
  try:
    return (
      book._replace(
        borrows=[o for o in book.borrows if o.id != order_id],
        lends=[o for o in book.lends if o.id != order_id]
      ),
      [o for o in book.lends + book.borrows if o.id == order_id][0]
    )
  except IndexError:
    return (book, None)
