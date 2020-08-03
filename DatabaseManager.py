# Database Manager
# Handles the data

# DATA STRUCTURE Item
# Stores item information
class Item():
    ItemID: int
    ItemName: str
    ItemDesc: str

# DATA STRUCTURE ORDER
# Stores user information.
class User():
    UserID: int
    Username: str

# DATA STRUCTURE ORDER
# Stores order information to be entered into the database
class Order():
    OrderID: int
    OrderContent : Item = []

# ITEM MANAGER
# Manages menu items within the database
class ItemManager():

    def AddItem(self, AddedItem:Item):
        pass

    def RemoveItem(self, RemovedItem:Item):
        pass

    def EditItem(self, OldItem:Item, NewItem:Item):
        pass


# ORDERING MANAGER
# Manages the orders as they are made
class OrderingManager():

    def PlaceOrder(self, PlacedOrder:Order):
        pass

    def CompleteOrder(self, Completed:Order):
        pass

    def RemoveOrder(self, RemovedOrder:Order):
        pass