# Database Manager
# Handles the data
import hashlib
import sqlite3
import enum
import json


# This is a macro function to return a cursor object to a specified database
def ConnectSQL(connect: str):
    sql = sqlite3.connect(connect)
    c = sql.cursor()
    return c, sql


# WARNING do not parse an object that is not a cursor it will break everything
# This is a macro to commit a cursors changes to the database
def CommitSQL(c):
    c.commit()
    c.close()


# DATA STRUCTURE Item
# Stores item information
class Item():
    ItemID: int
    ItemName: str
    ItemDesc: str
    ItemPrice: float
    ItemImage: str
    ItemCat: str
    TotalBought: str

    def __init__(self, ItemID: int = None, ItemName: str = None, ItemDesc: str = None, ItemPrice: float = None,
                 ItemImage: str = None, ItemCat: str = None, TotalBought: str = None):
        if ItemID != None:
            self.ItemID = ItemID
        if ItemName != None:
            self.ItemName = ItemName
        if ItemDesc != None:
            self.ItemDesc = ItemDesc
        if ItemPrice != None:
            self.ItemPrice = ItemPrice
        if ItemImage != None:
            self.ItemImage = ItemImage
        if ItemCat != None:
            self.ItemCat = ItemCat
        if TotalBought != None:
            self.TotalBought = TotalBought


# DATA STRUCTURE USER
# Stores user information.
class User:
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
    OrderName: str
    OrderContent: Item = []
    OrderActive: bool
    PickupTime: str
    PickupDate: int


# ENUM LoginErrorType
# :type FailedUsername
class ELoginErrorType(enum.Enum):
    FailedUsername = 0
    FailedPassword = 1
    FailedNone = 2
    FailedActive = 3
    FailedExist = 4


# ITEM MANAGER
# Manages menu items within the database


class ItemManager:
    Items = []

    def __init__(self):
        self.LoadItems()

    def AddItem(self, AddedItem: Item):
        pass

    def RemoveItem(self, RemovedItem: Item):
        pass

    def EditItem(self, OldItem: Item, NewItem: Item):
        pass

    def LoadItems(self):
        c, sql = ConnectSQL('main')
        c.execute("""SELECT * FROM Items""")
        for i in c.fetchall():
            LoadItem = Item(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            self.Items.append(LoadItem)

    @property
    def GetItems(self):
        return self.Items

    def SearchItems(self, search: str):
        SearchResult = []
        c = ConnectSQL('main')
        firstchar = search[0]
        query = firstchar + '%'
        c.execute("""SELECT * FROM Items WHERE ItemName LIKE ?""", (query,))
        stuff = c.fetchall()
        for i in stuff:
            print(i)
            LoadItem = Item(i[0], i[1], i[2], i[3], i[4], i[5], i[6])
            SearchResult.append(LoadItem)
        return SearchResult


# ORDERING MANAGER
# Manages the orders as they are made
class OrderingManager:

    Cart = []

    def __init__(self):
        print("Ordering Manager Initialised")

    def PlaceOrder(self, PlacedOrder: Order):
        c, sql = ConnectSQL('main')
        c.execute("""INSERT INTO Orders VALUES (?,?,True,?,?, ?)""", (
        PlacedOrder.OrderID, PlacedOrder.OrderName, PlacedOrder.OrderActive, PlacedOrder.PickupTime,
        PlacedOrder.PickupDate, PlacedOrder.OrderContent))
        CommitSQL(sql)



    def CompleteOrder(self, Completed: Order):
        pass

    def RemoveOrder(self, RemovedOrder: Order):
        pass

    def LoadActiveOrders(self):
        c, sql = ConnectSQL('Orders')
        c.execute("""SELECT * FROM Orders WHERE IsActive == True""")
        return c.fetchall()


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
        LoadedUser = User(UserData[0], UserData[1], UserData[2], UserData[3], UserData[4], UserData[5], UserData[6])
        return LoadedUser

    def LoadUserFromID(self, ID: int):
        sql = sqlite3.connect('main')
        c = sql.cursor()
        c.execute("""SELECT * FROM Users WHERE UserID =?""", (ID,))
        UserData = c.fetchall()[0]
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
            if str(self.Code.Encrypt(EnteredPass)) == str(result[0]):
                return True
            else:
                return ELoginErrorType.FailedPassword

        else:
            return ELoginErrorType.FailedActive

    def IsAdmin(self):
        pass


#

# Gets the table headers and returns them
# dont ask me why but the SQL interpreter doen't regocnise this SQL statement...

def GetTableHeaders(TableName: str):
    c, sql = ConnectSQL('main')
    c.execute("""PRAGMA table_info(Orders)""")
    output: list = []
    for i in c.fetchall():
        output.append(i[1])
    return output


print(GetTableHeaders('Orders'))


# :class EndpointManager
# Contains functionality to retrieve data from the the database
# and convert it into a JSON format
class EndpointManager:

    ## --- DATA GETTERS --- ##

    # This function will get the entire User entity
    # :return Retrieved user data
    @staticmethod
    def GetUserData():
        c, sql = ConnectSQL("main")
        c.execute("""SELECT COUNT(UserID) FROM Users WHERE IsActive == 1""")
        return c.fetchall()[0][0]

    # This static method will get the entire Orders entity
    # :return Retrieved data
    @staticmethod
    def GetOrderData():
        c, sql = ConnectSQL("main")
        c.execute("""SELECT * FROM Orders""")
        return c.fetchall()

    # This function will get the entire Items entity
    # :return Retrieved data
    @staticmethod
    def GetAllItems():
        c, sql = ConnectSQL("main")
        c.execute("""SELECT * FROM Items""")
        return c.fetchall()

    # This function will get all of the Additional Order Info Entity
    # :return Retrieved data
    @staticmethod
    def GetExtraOrderInfo():
        c, sql = ConnectSQL('main')
        c.execute("""SELECT * FROM AdditionalOrderInfo""")
        return c.fetchall()[0][0]

    ### - Processed Getters - ###

    # This static method will get all orders ever made
    # :return Retrieved data
    @staticmethod
    def GetCountTotalOrders():
        c, sql = ConnectSQL("main")
        c.execute("""SELECT COUNT(OrderID) FROM Orders""")
        return c.fetchall()[0][0]

    # This static method will get all current active orders
    # :return Retrieved data
    @staticmethod
    def GetCurrentOrderCount():
        c, sql= ConnectSQL("main")
        c.execute("""SELECT COUNT(OrderID) FROM Orders WHERE IsActive == 1""")
        return c.fetchall()[0][0]

    # This static method will count all the items currently on the menu
    # :return Retrieved data
    @staticmethod
    def GetItemCount():
        c, sql = ConnectSQL('main')
        c.execute("""SELECT COUNT(ItemID) FROM Items""")
        return c.fetchall()[0][0]

    # This static method will get the average of the price of all items on the menu
    # :return Retrieved data
    @staticmethod
    def GetAvgItemPrice():
        c, sql = ConnectSQL('main')
        c.execute("""SELECT AVG(ItemPrice) FROM Items""")
        return c.fetchall()[0][0]

    # This static method will get the sum of total bought for every item
    # :return Retrieved data
    @staticmethod
    def GetTotalBought():
        c, sql = ConnectSQL("main")
        c.execute("""SELECT SUM(TotalBought) FROM Items""")
        return c.fetchall()[0][0]

    ## --- SQL to JSON Data Conversion --- ##

    # Static method takes raw data from an entity and constructs a JSON formatted dictionary.
    # :param Data list with all the data to add
    # :param TableName name of entity which is being converted -> used to get the entity headers
    @staticmethod
    def ConvertData(Data, TableName):
        headers = GetTableHeaders(TableName)
        ConvertedData = {}
        for i in Data:
            new = zip(headers, i)
            ConvertedData[i[0]] = dict(new)
        return ConvertedData

    # :class JSON dict -> Overrides the __str__ method to return a properly JSON formatted dictionary with double quotes
    class JSONDict(dict):
        def __str__(self):
            return json.dumps(self)

    # Static method which fetches all the processed data and returns them as a tuple
    # :return Tuple constructed processed data
    @staticmethod
    def ConstructProcessedData():
        End = EndpointManager
        return End.GetUserData(), End.GetCountTotalOrders(), End.GetCurrentOrderCount(), End.GetItemCount(), End.GetAvgItemPrice(), End.GetTotalBought()

    # Joins the literal string headers for the processed data with the data inputted to create a dictionary object
    # :param Data The processed data which was retrieved
    # :return Constructed dictionary
    @staticmethod
    def ConvertProcessedData(Data):
        Headers = ("UserCount", "TotalOrders", "CurrentOrders", "ItemCount", "AverageItemPrice", "TotalItemsBought")
        return EndpointManager.JSONDict(zip(Headers, tuple(Data)))

    ## Testing stuff

    @staticmethod
    def LoadData():
        with open('raw.JSON', 'w') as JsonFile:
            return json.load(JsonFile.read())

    # This function will dump inputted data into the test.json file.
    @staticmethod
    def DumpData(data: dict):
        with open('test.json', 'w') as JsonFile:
            json.dump(data, JsonFile, indent=4)
