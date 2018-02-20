from unittest import TestCase

from pylend import completed_orders, new_contract, new_order, Side

class TestNewContract(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_valid_equal_rates_principles(self):
    contract = new_contract(
      new_order('A. Borrower', Side.BORROW, 10000, 5, 7),
      new_order('A. Lender', Side.LEND, 10000, 5, 7)
    )
    self.assertEqual(10000, contract.principle)
    self.assertEqual(5, contract.term)
    self.assertEqual(7, contract.rate)
    self.assertEqual('A. Borrower', contract.borrow.party)
    self.assertEqual(Side.BORROW, contract.borrow.side)
    self.assertEqual(10000, contract.borrow.principle)
    self.assertEqual(0, contract.borrow.leaves)
    self.assertEqual(5, contract.borrow.term)
    self.assertEqual(7, contract.borrow.rate)
    self.assertEqual('A. Lender', contract.lend.party)
    self.assertEqual(Side.LEND, contract.lend.side)
    self.assertEqual(10000, contract.lend.principle)
    self.assertEqual(0, contract.lend.leaves)
    self.assertEqual(5, contract.lend.term)
    self.assertEqual(7, contract.lend.rate)
    
  def test_asymmetric_rates_princples(self):
    contract = new_contract(
      new_order('A. Borrower', Side.BORROW, 8000, 5, 8),
      new_order('A. Lender', Side.LEND, 10000, 5, 7)
    )
    self.assertEqual(8000, contract.principle)
    self.assertEqual(5, contract.term)
    self.assertEqual(7.5, contract.rate)
    self.assertEqual('A. Borrower', contract.borrow.party)
    self.assertEqual(Side.BORROW, contract.borrow.side)
    self.assertEqual(8000, contract.borrow.principle)
    self.assertEqual(0, contract.borrow.leaves)
    self.assertEqual(5, contract.borrow.term)
    self.assertEqual(8, contract.borrow.rate)
    self.assertEqual('A. Lender', contract.lend.party)
    self.assertEqual(Side.LEND, contract.lend.side)
    self.assertEqual(10000, contract.lend.principle)
    self.assertEqual(2000, contract.lend.leaves)
    self.assertEqual(5, contract.lend.term)
    self.assertEqual(7, contract.lend.rate)

#TODO  completed_orders(contract/contracts) : generate set of completed orders
class TestCompletedOrders(TestCase):
  def setUp(self):
    self.maxDiff = None

  def test_both_sides_complete(self):
    b = new_order('A. Borrower', Side.BORROW, 10000, 5, 7)
    l = new_order('A. Lender', Side.LEND, 10000, 5, 7)
    self.assertEqual({b._replace(leaves=0), l._replace(leaves=0)},
      completed_orders(new_contract(b, l)))
      
  def test_borrow_complete(self):
    b = new_order('A. Borrower', Side.BORROW, 10000, 5, 7)
    l = new_order('A. Lender', Side.LEND, 15000, 5, 6)
    self.assertEqual({b._replace(leaves=0)},
      completed_orders(new_contract(b, l)))
      
  def test_lend_complete(self):
    b = new_order('A. Borrower', Side.BORROW, 12000, 5, 8)
    l = new_order('A. Lender', Side.LEND, 10000, 5, 7)
    self.assertEqual({l._replace(leaves=0)},
      completed_orders(new_contract(b, l)))
      
