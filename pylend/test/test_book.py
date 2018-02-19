from pylend import Side, new_book, new_order, add_order, cross, cross_all, \
  cancel_order

from unittest import TestCase

class TestBook(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_add_borrow_to_empty_book(self):
    book = new_book(5)
    b = new_order(None, Side.BORROW, 10000, 5, 7)
    book1 = add_order(book, b)
    self.assertFalse(book1.lends)
    self.assertEqual([b], book1.borrows)

  def test_add_lend_to_empty_book(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 7)
    book1 = add_order(book, l)
    self.assertFalse(book1.borrows)
    self.assertEqual([l], book1.lends)

  def test_add_borrow_to_bottom_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 7)
    b2 = new_order(None, Side.BORROW, 10000, 5, 6)
    book1 = add_order(book, b1)
    book2 = add_order(book1, b2)
    self.assertFalse(book2.lends)
    self.assertEqual([b1, b2], book2.borrows)

  def test_add_lend_to_bottom_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 7)
    l2 = new_order(None, Side.LEND, 10000, 5, 8)
    book1 = add_order(book, l1)
    book2 = add_order(book1, l2)
    self.assertFalse(book2.borrows)
    self.assertEqual([l1, l2], book2.lends)

  def test_add_borrow_to_top_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 6)
    b2 = new_order(None, Side.BORROW, 10000, 5, 7)
    book1 = add_order(book, b1)
    book2 = add_order(book1, b2)
    self.assertFalse(book2.lends)
    self.assertEqual([b2, b1], book2.borrows)

  def test_add_lend_to_top_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 8)
    l2 = new_order(None, Side.LEND, 10000, 5, 7)
    book1 = add_order(book, l1)
    book2 = add_order(book1, l2)
    self.assertFalse(book2.borrows)
    self.assertEqual([l2, l1], book2.lends)

  def test_add_borrow_to_bottom_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 6)
    b2 = new_order(None, Side.BORROW, 10000, 5, 8)
    b3 = new_order(None, Side.BORROW, 10000, 5, 7)
    book1 = add_order(book, b1)
    book2 = add_order(book1, b2)
    book3 = add_order(book2, b3)
    self.assertFalse(book3.lends)
    self.assertEqual([b2, b3, b1], book3.borrows)

  def test_add_lend_to_top_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 8)
    l2 = new_order(None, Side.LEND, 10000, 5, 6)
    l3 = new_order(None, Side.LEND, 10000, 5, 7)
    book1 = add_order(book, l1)
    book2 = add_order(book1, l2)
    book3 = add_order(book2, l3)
    self.assertFalse(book3.borrows)
    self.assertEqual([l2, l3, l1], book3.lends)

  #TODO preserve time priority or favour by size?

  def test_cross_empty_book(self):
    book = new_book(5)
    book1, contract = cross(book)
    self.assertTrue(contract is None)
    self.assertFalse(book1.lends)
    self.assertFalse(book1.borrows)

  def test_cross_no_borrows(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 8)
    book1 = add_order(book, l)
    book3, contract = cross(book1)
    self.assertTrue(contract is None)
    self.assertEqual([l], book3.lends)
    self.assertEqual([], book3.borrows)

  def test_cross_outside_margin(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 8)
    b = new_order(None, Side.BORROW, 10000, 5, 6)
    book1 = add_order(book, l)
    book2 = add_order(book1, b)
    book3, contract = cross(book2)
    self.assertTrue(contract is None)
    self.assertEqual([l], book3.lends)
    self.assertEqual([b], book3.borrows)

  def test_cross_exact_at_margin(self):
    book = new_book(5)
    l = new_order('L. Ender', Side.LEND, 10000, 5, 6)
    b = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    book1 = add_order(book, l)
    book2 = add_order(book1, b)
    book3, contract = cross(book2)
    self.assertEqual(10000, contract.principle)
    self.assertEqual(7, contract.rate)
    self.assertEqual(5, contract.term)
    self.assertEqual('L. Ender', contract.lend.party)
    self.assertEqual(Side.LEND, contract.lend.side)
    self.assertEqual(10000, contract.lend.principle)
    self.assertEqual(0, contract.lend.leaves)
    self.assertEqual(5, contract.lend.term)
    self.assertEqual(6, contract.lend.rate)
    self.assertEqual('B. Orrower', contract.borrow.party)
    self.assertEqual(Side.BORROW, contract.borrow.side)
    self.assertEqual(10000, contract.borrow.principle)
    self.assertEqual(0, contract.borrow.leaves)
    self.assertEqual(5, contract.borrow.term)
    self.assertEqual(8, contract.borrow.rate)
    self.assertFalse(book3.lends)
    self.assertFalse(book3.borrows)

  def test_cross_partial_borrow_at_margin(self):
    book = new_book(5)
    l = new_order('A. Lender Ltd.', Side.LEND, 10000, 5, 6)
    b = new_order('B. Orrower', Side.BORROW, 15000, 5, 8)
    book1 = add_order(book, l)
    book2 = add_order(book1, b)
    book3, contract = cross(book2)
    self.assertEqual(10000, contract.principle)
    self.assertEqual(7, contract.rate)
    self.assertEqual(5, contract.term)
    self.assertEqual('A. Lender Ltd.', contract.lend.party)
    self.assertEqual(Side.LEND, contract.lend.side)
    self.assertEqual(10000, contract.lend.principle)
    self.assertEqual(0, contract.lend.leaves)
    self.assertEqual(5, contract.lend.term)
    self.assertEqual(6, contract.lend.rate)
    self.assertEqual('B. Orrower', contract.borrow.party)
    self.assertEqual(Side.BORROW, contract.borrow.side)
    self.assertEqual(15000, contract.borrow.principle)
    self.assertEqual(5000, contract.borrow.leaves)
    self.assertEqual(5, contract.borrow.term)
    self.assertEqual(8, contract.borrow.rate)
    self.assertFalse(book3.lends)
    self.assertEqual(1, len(book3.borrows))
    self.assertEqual('B. Orrower', book3.borrows[0].party)
    self.assertEqual(Side.BORROW, book3.borrows[0].side)
    self.assertEqual(15000, book3.borrows[0].principle)
    self.assertEqual(5000, book3.borrows[0].leaves)
    self.assertEqual(5, book3.borrows[0].term)
    self.assertEqual(8, book3.borrows[0].rate)

  def test_cross_partial_lend_at_margin(self):
    book = new_book(5)
    l = new_order('L. Ender', Side.LEND, 15000, 5, 6)
    b = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    book1 = add_order(book, l)
    book2 = add_order(book1, b)
    book3, contract = cross(book2)
    self.assertEqual(10000, contract.principle)
    self.assertEqual(7, contract.rate)
    self.assertEqual(5, contract.term)
    self.assertEqual('L. Ender', contract.lend.party)
    self.assertEqual(Side.LEND, contract.lend.side)
    self.assertEqual(15000, contract.lend.principle)
    self.assertEqual(5000, contract.lend.leaves)
    self.assertEqual(5, contract.lend.term)
    self.assertEqual(6, contract.lend.rate)
    self.assertEqual('B. Orrower', contract.borrow.party)
    self.assertEqual(Side.BORROW, contract.borrow.side)
    self.assertEqual(10000, contract.borrow.principle)
    self.assertEqual(0, contract.borrow.leaves)
    self.assertEqual(5, contract.borrow.term)
    self.assertEqual(8, contract.borrow.rate)
    self.assertFalse(book3.borrows)
    self.assertEqual(1, len(book3.lends))
    self.assertEqual('L. Ender', book3.lends[0].party)
    self.assertEqual(Side.LEND, book3.lends[0].side)
    self.assertEqual(15000, book3.lends[0].principle)
    self.assertEqual(5000, book3.lends[0].leaves)
    self.assertEqual(5, book3.lends[0].term)
    self.assertEqual(6, book3.lends[0].rate)

  def test_cross_partial_lend_multiple_borrow(self):
    book = new_book(5)
    l = new_order('L. Ender', Side.LEND, 15000, 5, 6)
    b1 = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    b2 = new_order('A. N. Other', Side.BORROW, 8000, 5, 7)
    book = add_order(add_order(add_order(book, l), b1), b2)
    book1, contract1 = cross(book)
    book2, contract2 = cross(book1)
    book3, contract3 = cross(book2)
    self.assertEqual(10000, contract1.principle)
    self.assertEqual(5, contract1.term)
    self.assertEqual(7, contract1.rate)
    self.assertEqual(5000, contract2.principle)
    self.assertEqual(5, contract2.term)
    self.assertEqual(6.5, contract2.rate)
    self.assertEqual(None, contract3)
    self.assertEqual(book2, book3)
    #TODO: check books states?

  def test_cross_all_partial_lend_multiple_borrow(self):
    book = new_book(5)
    l = new_order('L. Ender', Side.LEND, 15000, 5, 6)
    b1 = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    b2 = new_order('A. N. Other', Side.BORROW, 8000, 5, 7)
    book = add_order(add_order(add_order(book, l), b1), b2)
    book1, contracts = cross_all(book)
    self.assertEqual(10000, contracts[0].principle)
    self.assertEqual(5, contracts[0].term)
    self.assertEqual(7, contracts[0].rate)
    self.assertEqual(5000, contracts[1].principle)
    self.assertEqual(5, contracts[1].term)
    self.assertEqual(6.5, contracts[1].rate)
    #TODO: check books states?

  def test_cancel_unfilled_only_borrow(self):
    book = new_book(5)
    b = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    book = add_order(book, b)
    self.assertEqual([b], book.borrows)
    book1, cancelled = cancel_order(book, b.id)
    self.assertEqual(b, cancelled)
    self.assertFalse(book1.borrows)
  #TODO: cancel with mutiple orders on the book

  def test_cancel_partially_filled(self):
    book = new_book(5)
    l = new_order('L. Ender', Side.LEND, 15000, 5, 6)
    b = new_order('B. Orrower', Side.BORROW, 10000, 5, 8)
    book, contract = cross(add_order(add_order(book, l), b))
    book_cancelled, order_cancelled = cancel_order(book, l.id)
    self.assertFalse(book_cancelled.lends)
    self.assertFalse(book_cancelled.borrows)
    self.assertEqual('L. Ender', order_cancelled.party)
    self.assertEqual(Side.LEND, order_cancelled.side)
    self.assertEqual(15000, order_cancelled.principle)
    self.assertEqual(5000, order_cancelled.leaves)
    self.assertEqual(5, order_cancelled.term)
    self.assertEqual(6, order_cancelled.rate)


#TODO firm/non-firm (borrow fully filled)

#TODO cancels? when can you cancel and what does it unwind?
# Cancelling a lend amends the principal to equal the leaves, contracts stand
# cancelling a borrow cancels all the associated contracts, lends may be added?