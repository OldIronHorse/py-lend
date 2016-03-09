#!/usr/bin/python

from py_lend import Book, Order, Party, Side
import unittest
from mock import Mock

class TestBook(unittest.TestCase):
  def test_add_borrow_to_empty_book(self):
    book = Book(5)
    b = Order(None, Side.BORROW, 10000, 5, 7)
    book.add(b)
    self.assertFalse(book.lends)
    self.assertEqual([b], book.borrows)

  def test_add_lend_to_empty_book(self):
    book = Book(5)
    l = Order(None, Side.LEND, 10000, 5, 7)
    book.add(l)
    self.assertFalse(book.borrows)
    self.assertEqual([l], book.lends)

  def test_add_borrow_to_bottom_of_bool(self):
    book = Book(5)
    b1 = Order(None, Side.BORROW, 10000, 5, 7)
    b2 = Order(None, Side.BORROW, 10000, 5, 6)
    book.add(b1)
    book.add(b2)
    self.assertFalse(book.lends)
    self.assertEqual([b1, b2], book.borrows)

  def test_add_lend_to_bottom_of_bool(self):
    book = Book(5)
    l1 = Order(None, Side.LEND, 10000, 5, 7)
    l2 = Order(None, Side.LEND, 10000, 5, 8)
    book.add(l1)
    book.add(l2)
    self.assertFalse(book.borrows)
    self.assertEqual([l1, l2], book.lends)


if __name__ == '__main__':
 unittest.main() 
