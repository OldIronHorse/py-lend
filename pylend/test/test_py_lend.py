from pylend import Side
from unittest import TestCase
from mock import Mock

class TestBook(TestCase):
  def test_add_borrow_to_empty_book(self):
    book = new_book(5)
    b = new_order(None, Side.BORROW, 10000, 5, 7)
    book.add(b)
    self.assertFalse(book.lends)
    self.assertEqual([b], book.borrows)

  def test_add_lend_to_empty_book(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 7)
    book.add(l)
    self.assertFalse(book.borrows)
    self.assertEqual([l], book.lends)

  def test_add_borrow_to_bottom_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 7)
    b2 = new_order(None, Side.BORROW, 10000, 5, 6)
    book.add(b1)
    book.add(b2)
    self.assertFalse(book.lends)
    self.assertEqual([b1, b2], book.borrows)

  def test_add_lend_to_bottom_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 7)
    l2 = new_order(None, Side.LEND, 10000, 5, 8)
    book.add(l1)
    book.add(l2)
    self.assertFalse(book.borrows)
    self.assertEqual([l1, l2], book.lends)

  def test_add_borrow_to_top_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 6)
    b2 = new_order(None, Side.BORROW, 10000, 5, 7)
    book.add(b1)
    book.add(b2)
    self.assertFalse(book.lends)
    self.assertEqual([b2, b1], book.borrows)

  def test_add_lend_to_top_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 8)
    l2 = new_order(None, Side.LEND, 10000, 5, 7)
    book.add(l1)
    book.add(l2)
    self.assertFalse(book.borrows)
    self.assertEqual([l2, l1], book.lends)

  def test_add_borrow_to_bottom_of_book(self):
    book = new_book(5)
    b1 = new_order(None, Side.BORROW, 10000, 5, 6)
    b2 = new_order(None, Side.BORROW, 10000, 5, 8)
    b3 = new_order(None, Side.BORROW, 10000, 5, 7)
    book.add(b1)
    book.add(b2)
    book.add(b3)
    self.assertFalse(book.lends)
    self.assertEqual([b2, b3, b1], book.borrows)

  def test_add_lend_to_top_of_book(self):
    book = new_book(5)
    l1 = new_order(None, Side.LEND, 10000, 5, 8)
    l2 = new_order(None, Side.LEND, 10000, 5, 6)
    l3 = new_order(None, Side.LEND, 10000, 5, 7)
    book.add(l1)
    book.add(l2)
    book.add(l3)
    self.assertFalse(book.borrows)
    self.assertEqual([l2, l3, l1], book.lends)

  #TODO preserve time priority or favour by size?

  def test_cross_empty_book(self):
    book = new_book(5)
    contract = book.cross(1)
    self.assertTrue(contract is None)
    self.assertFalse(book.lends)
    self.assertFalse(book.borrows)

  def test_cross_outside_margin(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 8)
    b = new_order(None, Side.BORROW, 10000, 5, 6)
    book.add(l)
    book.add(b)
    contract = book.cross(1)
    self.assertTrue(contract is None)
    self.assertEqual([l], book.lends)
    self.assertEqual([b], book.borrows)

  def test_cross_exact_at_margin(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 6)
    b = new_order(None, Side.BORROW, 10000, 5, 8)
    book.add(l)
    book.add(b)
    contract = book.cross(2)
    self.assertEqual(10000, contract.amount)
    self.assertEqual(l, contract.lend)
    self.assertEqual(b, contract.borrow)
    self.assertTrue(contract.firm)
    self.assertFalse(book.lends)
    self.assertFalse(book.borrows)
    self.assertEqual(0, l.leaves)
    self.assertEqual(0, b.leaves)

  def test_cross_partial_borrow_at_margin(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 10000, 5, 6)
    b = new_order(None, Side.BORROW, 15000, 5, 8)
    book.add(l)
    book.add(b)
    contract = book.cross(2)
    self.assertEqual(10000, contract.amount)
    self.assertEqual(l, contract.lend)
    self.assertEqual(b, contract.borrow)
    self.assertFalse(contract.firm)
    self.assertFalse(book.lends)
    self.assertEqual([b], book.borrows)
    self.assertEqual(0, l.leaves)
    self.assertEqual(5000, b.leaves)

  def test_cross_partial_lend_at_margin(self):
    book = new_book(5)
    l = new_order(None, Side.LEND, 15000, 5, 6)
    b = new_order(None, Side.BORROW, 10000, 5, 8)
    book.add(l)
    book.add(b)
    contract = book.cross(2)
    self.assertEqual(10000, contract.amount)
    self.assertEqual(l, contract.lend)
    self.assertEqual(b, contract.borrow)
    self.assertTrue(contract.firm)
    self.assertFalse(book.borrows)
    self.assertEqual([l], book.lends)
    self.assertEqual(0, b.leaves)
    self.assertEqual(5000, l.leaves)

#TODO cancels? when can you cancel and what does it unwind?
# Cancelling a lend amends the principal to equal the leaves, contracts stand
# cancelling a borrow cancels all the associated contracts, lends may be added?
