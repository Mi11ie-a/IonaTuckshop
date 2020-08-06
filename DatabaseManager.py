# Database Manager
# Handles the data

import sqlite3
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
    Password: str
    ContactEmail: str
    IsActive: bool


    is_authenticated: bool
    is_active: bool
    is_anonymous: bool

    def __init__(self, Username:str, Password:str):
        self.Username = Username
        self.Password = Password
    def get_id(self):
        return self.UserID

# DATA STRUCTURE ORDER
# Stores order information to be entered into the database
class Order():
    OrderID: int
    OrderContent : Item = []
    OrderActive: bool


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

    def __init__(self):
        print("Ordering Manager Initialised")

    def PlaceOrder(self, PlacedOrder:Order):
        pass

    def CompleteOrder(self, Completed:Order):
        pass

    def RemoveOrder(self, RemovedOrder:Order):
        pass


class EncryptionManager():

    def Encrypt(self, ToEncrypt: str):
        pass

class UserManager():

    Code : EncryptionManager
    CurrentUser: User

    # METHODS
    def __init__(self, User:User):
        Code = EncryptionManager()
        self.CurrentUser = User
        print("User Manager Initialised")

    def get_id(self):


    #Uses the username to get the user ID from the data base (first auth check)
    def FindUser(self, User:User):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT Username FROM users WHERE Username = ?""", (User.Username))
        if c.fetchone() != None:
            return True
        else:
            return False

    def LoadUser(self, ID:int):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT * FROM Users WHERE UserID =?""", (ID))
        return c.fetchall()

    def GetUserID(self):
        return self.CurrentUser.UserID

    def LoginUser(self, User:User):
        if User.IsActive == True:
            sql = sqlite3.connect('main')
            c = sql.cursor()
            c.execute("""SELECT Password FROM users WHERE UserID = (?)""", (User.UserID,))
            if self.Code.Encrypt(User.Password) == c.fetchone():
                return True
            else:
                return False
        else:
            return False


class EndpointManager():

    def DoStuff(self):
        pass