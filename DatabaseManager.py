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
    is_active: bool

    is_authenticated: bool
    is_active: bool
    is_anonymous: bool
    IsAdmin: bool

    def __init__(self, UserID: int = None, Username: str = None, Password: str = None, IsActive: bool = None,
                 ContactEmail: str = None, StudentID: int = None, IsAdmin: bool = False):
        if UserID != None:
            self.UserID = UserID
        if Username != None:
            self.Username = Username
        if Password != None:
            self.Password = Password
        if ContactEmail != None:
            self.ContactEmail = ContactEmail
        if IsActive != None:
            self.is_active = IsActive
        if IsAdmin != None:
            self.IsAdmin = IsAdmin


    def get_id(self):
        return self.UserID

    def is_authenticated(self):
        return self.is_authenticated

# DATA STRUCTURE ORDER
# Stores order information to be entered into the database
class Order():
    OrderID: int
    OrderContent: Item = []
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
    Items: Item = []

    def AddItem(self, AddedItem: Item):
        pass

    def RemoveItem(self, RemovedItem: Item):
        pass

    def EditItem(self, OldItem: Item, NewItem: Item):
        pass

    @property
    def GetItems(self):
        return self.Items


# ORDERING MANAGER
# Manages the orders as they are made
class OrderingManager:

    def __init__(self):
        print("Ordering Manager Initialised")

    def PlaceOrder(self, PlacedOrder: Order):
        pass

    def CompleteOrder(self, Completed: Order):
        pass

    def RemoveOrder(self, RemovedOrder: Order):
        pass


class EncryptionManager:

    def Encrypt(self, ToEncrypt: str):
        salt = b'm\xe6%\x83,\xc1&\xa2\\s\x7fj\xb4\xfa\xcenZ&+\x7f\xe5\xbbx?/H\xe0\xabz-e\x0e'
        key = hashlib.pbkdf2_hmac(
            'sha256',
            ToEncrypt.encode('utf-8'),
            salt,
            100000
        )
        return key


class UserManager:
    Code: EncryptionManager = EncryptionManager()
    CurrentUser: User

    # METHODS
    def __init__(self, User: User = None):
        Code = EncryptionManager()
        self.CurrentUser = User
        print("User Manager Initialised")

    @property
    def get_id(self):
        return self.CurrentUser.UserID

    # Uses the username to get the user ID from the data base (first auth check)
    def FindUser(self, CheckUser: str):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT Username FROM users WHERE Username = (?)""", (CheckUser,))
        if c.fetchone() != None:
            return True
        else:
            return False

    def LoadUser(self, Username: str):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT * FROM Users WHERE Username =?""", (Username,))
        UserData = c.fetchall()[0]
        print(UserData)
        LoadedUser = User(UserData[0], UserData[1], UserData[2], UserData[3], UserData[4], UserData[5], UserData[6])
        return LoadedUser


    def LoadUserFromID(self, ID: int):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT * FROM Users WHERE UserID =?""", (ID,))
        UserData = c.fetchall()[0]
        print(UserData)
        LoadedUser = User(UserData[0], UserData[1], UserData[2], UserData[3], UserData[4], UserData[5], UserData[6])
        return LoadedUser

    def GetUserID(self):
        return self.CurrentUser.UserID

    def LoginUser(self, User: User, EnteredPass: str):
        if User.is_active == True:
            sql = sqlite3.connect('main')
            c = sql.cursor()
            c.execute("""SELECT Password FROM users WHERE UserID = (?)""", (User.UserID,))
            result = c.fetchone()
            print("Index 0: " + result[0])
            if str(self.Code.Encrypt(EnteredPass)) == str(result[0]):
                print("Password was the same YAY")
                return True
            else:
                print("Password Failed")
                return ELoginErrorType.FailedPassword

        else:
            print("Failed Active")
            return ELoginErrorType.FailedActive


    def IsAdmin(self):
        pass


#
def ConnectSQL(connect: str):
    sql = sqlite3.connect(connect)
    c = sql.cursor()
    return c


# WARNING do not parse an object that is not a cursor it will break everything
# This is a maco to commit a cursors changes to the database
def CommitSQL(c):
    c.commit()
    c.close()


def GetTableHeaders(TableName: str):
    c = ConnectSQL('main')
    c.execute("""PRAGMA table_info(Orders)""")
    output: list = []
    for i in c.fetchall():
        output.append(i[1])
    print(output)
    return output


class EndpointManager():

    @staticmethod
    def ConvertToJson(Category: str, data, table: str = None):
        if table != None:
            headers = GetTableHeaders(table)
            HeaderDict = {}
            for i in headers:
                HeaderDict[i] = {}
            print(HeaderDict)
            HeaderDictString = str(HeaderDict)
            HeaderDictString = HeaderDictString.replace('{', '')
            HeaderDictString = HeaderDictString.replace('}', '')
            print("HeaderDICT: " + HeaderDictString)
            string = {Category:{
                HeaderDictString:{}
            }}
            return string
        else:
            for i in data:
                string = {Category: str(i)}
                print(string)
            return string

    @staticmethod
    def DumpData(data: dict):
        with open('test.json', 'w') as JsonFile:
            json.dump(data, JsonFile, indent=4)

    def UpdateData(self, Category: str, data: dict):
        pass

    @staticmethod
    def GetUserData():
        c = ConnectSQL("maindb")
        c.execute("""SELECT COUNT(IsActive = True) FROM Users""")
        return c.fetchall()

    @staticmethod
    def GetOrderData():
        c = ConnectSQL("maindb")
        c.execute("""SELECT * FROM Orders""")
        return c.fetchall()

    @staticmethod
    def GetCountTotalOrders():
        c = ConnectSQL("maindb")
        c.execute("""SELECT COUNT(OrderID) FROM Orders""")

    @staticmethod
    def GetCurrentOrderCount():
        c = ConnectSQL("maindb")
        c.execute("""SELECT COUNT(OrderID) FROM Orders WHERE IsActive = TRUE""")
        return c.fetchall()

    @staticmethod
    def GetAllOrderCount():
        c = ConnectSQL("maindb")
        c.execute("""SELECT COUNT(OrderID) FROM Orders""")
        return c.fetchall()

    @staticmethod
    def GetItemCount():
        c = ConnectSQL('maindb')
        c.execute("""SELECT COUNT(ItemID) FROM Items""")
        return c.fetchall()

    @staticmethod
    def GetAvgItemPrice():
        c = ConnectSQL('maindb')
        c.execute("""SELECT AVG(ItemPrice) FROM Items""")
        return c.fetchall()

    @staticmethod
    def GetTotalBought():
        c = ConnectSQL("maindb")
        c.execute("""SELECT SUM(TotalBought) FROM Items""")
        return c.fetchall()

    @staticmethod
    def GetAllOrders():
        c = ConnectSQL("main")
        print(c)
        c.execute("""SELECT * FROM Orders""")
        return c.fetchall()



