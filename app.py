from flask import Flask, render_template, session, request, redirect,url_for
from DatabaseManager import OrderingManager, ItemManager, UserManager, User, Item
from flask_login import login_manager, login_required, login_user
app = Flask(__name__)

# Init all managers
#OrderMan = OrderingManager()
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
    return render_template('test.html')

@app.route('/loginredirect', methods=['POST'])
def Login():
    if request.method == "POST":
        EnteredP = request.form['Password']
        EnteredU = request.form['Username']
        if UserMan.FindUser(EnteredU) != False:
            NewUser = UserMan.LoadUser(EnteredU)
            if UserMan.LoginUser(NewUser, EnteredP) == True:
                login_user(NewUser) # Authenticate the use with Flask
                UserMan.CurrentUser = NewUser # Autheticate the user with the  manager
                print("Authorised")
                return redirect(url_for('Menu'))
            else:
                return redirect(url_for('Landing'))
        else:
            return redirect(url_for('Landing'))
    else:
        return redirect(url_for('Landing'))

@loginman.user_loader
def load_user(user_id):
    return UserMan.LoadUserFromID(user_id)



if __name__ == '__main__':
    app.run()
