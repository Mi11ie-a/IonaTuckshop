### Iona Tuckshop : App.py ###
"""
Author: Anthony Kirn
Description: Main Flask application. Handles routes and frontend web functionality

"""

# Imports
from flask import Flask, render_template, session, request, redirect, url_for
from DatabaseManager import OrderingManager, ItemManager, UserManager, User, Item, GetTableHeaders, EndpointManager
from flask_login import login_manager, login_required, login_user, logout_user

# DEFINE app as Flask instance
app = Flask(__name__)

# Init all managers
OrderMan = OrderingManager()
UserMan = UserManager()
ItemMan = ItemManager()

# Init the Flask login manager
loginman = login_manager.LoginManager()

# Register the login manager with the Flask app
loginman.init_app(app)

# Set Secret key of Flask app
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# :route / -> Main landing page of website
@app.route('/')
def Landing():
    return render_template('index.html')

# :route '/login' -> Login page of application
@app.route('/login')
def LoginPage():
    return render_template('signin.html')

# :route '/menu/<search>' -> Tuckshop menu page
# :param search:Item -> The item to display from search results
# :login_required -> Registers with login manager that the user is required to be authenticated
@app.route('/menu/<search>')
@login_required
def Menu(search:Item):
    if search != 'NULL':
        return render_template('items.html', items=search)
    else:
        return render_template('items.html', items=ItemMan.Items)

# :route '/loginredirect' -> Authenticates the user
@app.route('/loginredirect', methods=['POST'])
def Login():
    if request.method == "POST":
        EnteredP = request.form['Password']
        EnteredU = request.form['Username']
        if UserMan.FindUser(EnteredU) != False:
            NewUser = UserMan.LoadUser(EnteredU)
            if UserMan.LoginUser(NewUser, EnteredP) == True:
                login_user(NewUser)  # Authenticate the use with Flask
                UserMan.CurrentUser = NewUser  # Autheticate the user with the  manager
                return redirect(url_for('Menu', search='NULL'))
            else:
                return redirect(url_for('Landing'))
        else:
            return redirect(url_for('Landing'))
    else:
        return redirect(url_for('Landing'))

# :route '/userlogout' -> Logs the user out of the session
@app.route('/userlogout')
def LogoutUser():
    logout_user()
    return redirect(url_for('Landing'))

# :route '/searchmenu' -> Queries database for search query
@app.route('/searchmenu', methods=['POST', 'GET'])
def SearchMenu():
    if request.method == 'POST':
        query = request.form['Search']
        ItemMan.SearchItems(query)
        return redirect(url_for('Menu', search=ItemMan.SearchItems(query)))
    else:
        return redirect(url_for('Menu', search='NULL'))


## -- Flask Endpoints -- ##

# Return the entire order table in JSON format to '/orderdata'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/orderdata')
def GetOrderData():
    return render_template('endpoints.html', json=EndpointManager.ConvertData(EndpointManager.GetOrderData(), "Orders"))


# Return the entire items entity in JSON format to '/itemdata'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/itemdata')
def GetItemData():
    return render_template('endpoints.html', json=EndpointManager.ConvertData(EndpointManager.GetAllItems(), 'Items'))


# Return the entire extra order info entity in JSON format to '/extraorderinfo'
# :return render_template -> 'endpoints.html' with a data payload
@app.route('/extraorderinfo')
def GetExtraOrderInfo():
    return render_template('endpoints.html',
                           json=EndpointManager.ConvertData(EndpointManager.GetExtraOrderInfo(), 'AdditionalOrderInfo'))


# Return the processed data from the databases in JSON format
# :return  render_template -> 'endpoints.html' with a data payload
@app.route('/processedata')
def GetProcessed():
    return render_template('endpoints.html',
                           json=EndpointManager.ConvertProcessedData(EndpointManager.ConstructProcessedData()))


# Check to see if the user is still valid
# :param user_id:int -> The id of the user to check
@loginman.user_loader
def load_user(user_id):
    return UserMan.LoadUserFromID(user_id)


if __name__ == '__main__':
    app.run()



