# Database Manager
# Handles the data
import hashlib
import sqlite3
import enum
import json
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

    def __init__(self, UserID:int = None, Username:str = None, Password:str = None, ContactEmail:str = None, IsActive:bool = None,):
        if UserID != None:
            self.UserID = UserID
        if Username != None:
            self.Username = Username
        if Password != None:
            self.Password = Password
        if ContactEmail != None:
            self.ContactEmail = ContactEmail
        if IsActive != None:
            self.IsActive = IsActive

    def get_id(self):
        return self.UserID

# DATA STRUCTURE ORDER
# Stores order information to be entered into the database
class Order():
    OrderID: int
    OrderContent : Item = []
    OrderActive: bool

class ELoginErrorType(enum.Enum):
    FailedUsername = 0
    FailedPassword = 1
    FailedNone = 2
    FailedActive = 3
    FailedExist = 4

# ITEM MANAGER
# Manages menu items within the database


class ItemManager:

    def AddItem(self, AddedItem:Item):
        pass

    def RemoveItem(self, RemovedItem:Item):
        pass

    def EditItem(self, OldItem:Item, NewItem:Item):
        pass


# ORDERING MANAGER
# Manages the orders as they are made
class OrderingManager:

    def __init__(self):
        print("Ordering Manager Initialised")

    def PlaceOrder(self, PlacedOrder:Order):
        pass

    def CompleteOrder(self, Completed:Order):
        pass

    def RemoveOrder(self, RemovedOrder:Order):
        pass


class EncryptionManager:

    def Encrypt(self, ToEncrypt: str):
        pass


class UserManager:

    Code : EncryptionManager
    CurrentUser: User

    # METHODS
    def __init__(self, User:User = None):
        Code = EncryptionManager()
        self.CurrentUser = User
        print("User Manager Initialised")

    def get_id(self):
        pass

    #Uses the username to get the user ID from the data base (first auth check)
    def FindUser(self, User:User):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT Username FROM users WHERE Username = ?""", (User.Username))
        if c.fetchone() != None:
            return c.fetchone()
        else:
            return None

    def LoadUser(self, ID:int):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT * FROM Users WHERE UserID =?""", (ID,))
        for i in c.fetchone():
            LoadedUser = User(i[0], i[1], i[2], i[3], i[4], i[5])
        return LoadedUser

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
                return ELoginErrorType.FailedPassword
        else:
            return ELoginErrorType.FailedActive

import collections
class EndpointManager():

    def ConvertToJson(self, Category:str, data:collections.defaultdict):
        data[Category]
        return data

    def DumpData(self, data):
        with open('test.json', 'w') as JsonFile:
            json.dump(data, JsonFile, indent=4)


data = {
    "bad": {
    "Hello": 1,
    "You": 2,
    "Are": 3,
    "Stupid": 4
}

}
man = EndpointManager()

print(man.ConvertToJson("Hello", data))