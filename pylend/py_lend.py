#!/usr/bin/python

from enum import Enum

Side = Enum('Side', 'BORROW LEND')

class Party:
  def __init__(self, name):
    self.name = name
    self.orders = []
    
class Order:
  def __init__(self, party, side, principal, term, rate):
    self.party = party
    self.side = side
    self.principal = principal
    self.leaves = principal
    self.term = term
    self.rate = rate
    self.contracts = []

  def fill(self, contract):
    self.leaves -= contract.amount
    self.contracts.append(contract)
    if self.side == Side.BORROW and self.leaves == 0:
      contract.firm = True

class Contract:
  def __init__(self, amount, borrow, lend):
    self.amount = amount
    self.borrow = borrow
    self.lend = lend
    self.firm = False

class Book:
  def __init__(self, term):
    self.term = term
    self.borrows = []
    self.lends = []
  
  def add(self, order):
    {Side.BORROW: lambda: self.borrows.append(order),
     Side.LEND: lambda: self.lends.append(order)}[order.side]()
    self.borrows.sort(key=lambda o: o.rate, reverse=True)
    self.lends.sort(key=lambda o: o.rate)

  def cross(self, margin):
    try:
      borrow = self.borrows[0]
      lend = self.lends[0]
      if borrow.rate - lend.rate >= margin:
        quantity = min(borrow.leaves, lend.leaves)
        contract = Contract(quantity, borrow, lend)
        borrow.fill(contract)
        lend.fill(contract)
        if borrow.leaves == 0:
          self.borrows = self.borrows[1:]
        if lend.leaves == 0:
          self.lends = self.lends[1:]
        return contract
      else:
        return None
    except(IndexError):
      return None
