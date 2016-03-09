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
