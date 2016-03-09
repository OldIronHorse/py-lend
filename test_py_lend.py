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


if __name__ == '__main__':
 unittest.main() 
