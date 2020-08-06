from flask import Flask, render_template, session, request, redirect,url_for
from DatabaseManager import OrderingManager, ItemManager, UserManager, User, Item
from flask_login import login_manager, login_required
app = Flask(__name__)

# Init all managers
OrderMan = OrderingManager()
UserMan = UserManager()

loginman = login_manager.LoginManager()
loginman.init_app(app)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def Landing():
    return render_template('base.html')


@app.route('/menu')
@login_required
def Menu():
    return render_template('base.html')

@app.route('loginredirect', methods=['GET', 'POST'])
def Login():
    Username = request.form['Username']
    Password = request.form['Password']
    NewUser = User(Username, Password)
    if UserMan.FindUser(NewUser) == True:
        UserMan.LoadUser()


def LoadUser(UserID):
    return UserManager.GetUserID()

if __name__ == '__main__':
    app.run()
