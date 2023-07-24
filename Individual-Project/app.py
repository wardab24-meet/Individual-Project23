
from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyASf3Jp1lbB4qgBw-LWhbcYYDKL9G3cZJM",
    "authDomain": "miniproject-168f0.firebaseapp.com",
    "projectId": "miniproject-168f0",
    "storageBucket": "miniproject-168f0.appspot.com",
    "messagingSenderId": "1071357410059",
    "appId": "1:1071357410059:web:fe374bc107b3a04acf400e",
    "measurementId": "G-TLGT1J456W",
    "databaseURL": "https://miniproject-168f0-default-rtdb.europe-west1.firebasedatabase.app/"
}   

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # try:
        auth.sign_in_with_email_and_password(email, password)
        login_session['user'] =  auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('profile'))
        # except:
            # pass
            # flash("Invalid credentials. Please try again.", "error")
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            db.child('users').child(login_session['user']['localId']).set({'email': email})
            # flash("Account created successfully!", "success")
            return redirect(url_for('login'))
        except:
            pass
            # flash("Account creation failed. Please try again.", "error")
    return render_template("signup.html")

@app.route('/profile')
def profile():
    if 'user' in login_session:
        profile = db.child('users').child(login_session['user']['localId']).get().val()
        email=profile['email']
        # user = auth.get_account_info(session['user'])
        # email = user['users'][0]['email']
        return render_template("profile.html", email=email)
    else:
        # flash("Please login first.", "error")
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    login_session.pop('user', None)
    # flash("You have been logged out.", "success")
    return redirect(url_for('login'))


@app.route('/shop')
def shop():
    # In-memory product data store (you can replace this with a real database)
    products = [
        {
            'name': 'Product 1',
            'price': 10.99,
            'image': 'images/product1.jpg',
            'description': 'This is product 1.'
        },
        {
            'name': 'Product 2',
            'price': 15.99,
            'image': 'images/product2.jpg',
            'description': 'This is product 2.'
        },
        # Add more products as needed
    ]

    return render_template('shop.html', products=products)
    return "WELCOME TO THE STTRRREEEEE"

if __name__ == '__main__':
    app.run(debug=True)