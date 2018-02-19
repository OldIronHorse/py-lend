from collections import namedtuple

from .order import Side
from .contract import Contract

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
  return adders[order.side](book, order);

def cross(book):
  try:
    if book.borrows[0].rate >= book.lends[0].rate:
      contract_amount = min(book.borrows[0].leaves, book.lends[0].leaves)
      new_borrow = book.borrows[0]._replace(
          leaves=book.borrows[0].leaves - contract_amount)
      new_lend = book.lends[0]._replace(
          leaves=book.lends[0].leaves - contract_amount)
      contract=Contract(
        borrow=new_borrow,
        lend=new_lend,
        term=book.term,
        rate=(book.borrows[0].rate + book.lends[0].rate) / 2,
        principle=contract_amount
      )
      new_borrows = book.borrows[1:]
      if new_borrow.leaves > 0:
        new_borrows = [new_borrow] + new_borrows
      new_lends = book.lends[1:]
      if new_lend.leaves > 0:
        new_lends = [new_lend] + new_lends
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
  return (
    book._replace(
      borrows=[o for o in book.borrows if o.id != order_id],
      lends=[o for o in book.lends if o.id != order_id]
    ),
    [o for o in book.lends + book.borrows if o.id == order_id][0]
  )
