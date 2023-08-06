#  Copyright (c) 2021 | KingKevin23 (@kingkevin023)

class OrderException(Exception): pass

class OrderCreationException(OrderException): pass

class OrderDeletionException(OrderException): pass